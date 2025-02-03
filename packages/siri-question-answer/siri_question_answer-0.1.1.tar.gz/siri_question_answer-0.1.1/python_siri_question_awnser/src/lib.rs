use pyo3::prelude::*;
use pyo3::types::PyString;
use siri_question_response::listeners::estimated_time_table::EstimatedTableListerner;
use tokio::sync::mpsc::unbounded_channel;
use std::sync::Arc;


#[pyclass]
#[derive(Debug, Clone)]
pub struct EstimatedTableConsumer {
    url: String,
}

#[pymethods]
impl EstimatedTableConsumer {
    #[new]
    pub fn new(url: String) -> Self {
        EstimatedTableConsumer { url }
    }

    fn listen_estimated_timetable(
        &self,
        interval: u64,
        callback: PyObject,
    ) -> PyResult<()> {
        // Clone values for move into thread
        let url = self.url.clone();
        let lines = vec!["7", "8", "9", "10", "11", "12", "20", "21", "22", "23", "24", "51", "52", "53", "54", "55", "56", "57", "58", "59", "61", "62", "63", "64", "65"].iter().map(|s| s.to_string()).collect();
        let callback = Arc::new(callback);

        // Spawn a dedicated thread for async operations
        std::thread::spawn(move || {
            // Create Tokio runtime inside the thread
            let rt = tokio::runtime::Runtime::new().unwrap();
            
            // Main async block
            rt.block_on(async move {
                let (tx, mut rx) = unbounded_channel();

                // Start the listener
                let listener_handle = EstimatedTableListerner::run(
                    url,
                    lines,
                    interval,
                    tx.clone(),
                );

                // Handle incoming notifications
                let receiver_handle = tokio::spawn(async move {
                    while let Some(notification) = rx.recv().await {                        
                        Python::with_gil(|py| {
                            let args = (
                                PyString::new(py, &notification.message).into_pyobject(py),
                                PyString::new(py, &notification._type).into_pyobject(py),
                                PyString::new(py, &uuid::Uuid::new_v4().to_string()).into_pyobject(py),
                            );
                            let args = (args.0.unwrap(), args.1.unwrap(), args.2.unwrap());
                            // wait 1s before calling the callback
                            std::thread::sleep(std::time::Duration::from_secs(1));
                            if let Err(e) = callback.call1(py, args) {
                                e.print_and_set_sys_last_vars(py);
                            }
                        });
                    }
                });

                // Keep both tasks running
                let _ = tokio::join!(listener_handle, receiver_handle);
            });
        });

        Ok(())
    }
}



/// A Python module implemented in Rust.
#[pymodule]
fn siri_question_answer(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<EstimatedTableConsumer>()?;
    Ok(())
}
