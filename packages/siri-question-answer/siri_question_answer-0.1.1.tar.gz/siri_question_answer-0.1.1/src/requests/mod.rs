pub mod lines_dicovery;
pub mod estimated_table;


#[derive(Debug)]
pub struct SoapRequestParams {
    pub timestamp: String,
    pub requestor_ref: String,
    pub message_id: String,
}

