use tokio::sync::mpsc::UnboundedSender;

use crate::{requests::{estimated_table::EstimatedTableRequest, SoapRequestParams}, send_soap_request, Notification};


pub struct EstimatedTableListerner;


impl EstimatedTableListerner {
    pub fn run(url: String, lines: Vec<String>, interval: u64, sender: UnboundedSender<Notification>) -> tokio::task::JoinHandle<()> {
        tokio::spawn(async move {
            let mut interval = tokio::time::interval(tokio::time::Duration::from_secs(interval));
            loop {
                interval.tick().await;
                let id = uuid::Uuid::new_v4();
                let date = chrono::Utc::now();
                let requestor_ref = "Hove";
                let message_id = format!("{}::Message::{}", requestor_ref, id.to_string());
                let soap_params = SoapRequestParams {
                    timestamp: date.to_rfc3339(),
                    requestor_ref: "HOVE".to_string(),
                    message_id,
                };

                let request = EstimatedTableRequest::new(soap_params);
                let result = request.create_estimated_table_request(lines.clone()).unwrap();

                let client = reqwest::Client::new();
                let response = send_soap_request(&client, &url, &result).await.expect("Failed to send request");
                let body = response.text().await.expect("Failed to get response body");
                let vjs = crate::transformers::split_vjs::split_soap_envelopes(&body).expect("Failed to split SOAP envelopes");

                for envelope in vjs {
                    sender.send(Notification {
                        message: envelope,
                        _type: "EstimatedTable".to_string(),
                    }).expect("Failed to send notification");
                }
            }
        })
    }
}