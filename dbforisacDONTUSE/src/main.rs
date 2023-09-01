use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use warp::Filter;

#[derive(Debug, Serialize, Deserialize, Clone)]
struct ResponseData {
    success: bool,
    status_code: u16,
    status_message: String,
}

struct DataHandlerMutex {
    lock: RwLock<DataHandler>,
}

#[derive(Debug, Serialize, Deserialize)]
struct DataHandler {
    data: HashMap<String, HashMap<String, String>>,
}

impl DataHandlerMutex {
    fn new() -> Self {
        DataHandlerMutex {
            lock: RwLock::new(DataHandler::new()),
        }
    }
}

impl DataHandler {
    fn new() -> Self {
        DataHandler {
            data: HashMap::new(),
        }
    }
    async fn get_serializable_data(&self) -> HashMap<String, HashMap<String, String>> {
        self.data.clone()
    }
    async fn read_data(&self, directory: &str) -> ResponseData {
        if let Some(inner) = self.data.get(directory) {
            ResponseData {
                success: true,
                status_code: 200,
                status_message: "Data Successfully Found!".to_string(),
            }
        } else {
            ResponseData {
                success: false,
                status_code: 404,
                status_message: "Data Not Found!".to_string(),
            }
        }
    }

    async fn set_data(&mut self, directory: &str, value: String) -> ResponseData {
        let inner = self
            .data
            .entry(directory.to_string())
            .or_insert_with(HashMap::new);
        inner.insert("value".to_string(), value);

        ResponseData {
            success: true,
            status_code: 200,
            status_message: "Data Set Successfully!".to_string(),
        }
    }

    async fn delete_data(&mut self, directory: &str) -> ResponseData {
        if let Some(inner) = self.data.remove(directory) {
            ResponseData {
                success: true,
                status_code: 200,
                status_message: "Data Deleted Successfully!".to_string(),
            }
        } else {
            ResponseData {
                success: false,
                status_code: 404,
                status_message: "Data Not Found!".to_string(),
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let data_handler = Arc::new(DataHandlerMutex::new());
    let data_ref1 = Arc::clone(&data_handler);
    let data_ref2 = Arc::clone(&data_handler);
    let data_ref3 = Arc::clone(&data_handler);

    let routes = warp::path!(String)
        .and(warp::get())
        .and_then(move |data_file_path: String| {
            let data_ref = Arc::clone(&data_ref1);
            async move {
                let response = data_ref.lock.read().await.read_data(&data_file_path).await;
                Ok::<warp::reply::Json, warp::Rejection>(warp::reply::json(&response))
            }
        })
        .or(warp::path!(String)
            .and(warp::post())
            .and(warp::body::json())
            .and_then(
                move |data_file_path: String, value: HashMap<String, String>| {
                    let data_ref = Arc::clone(&data_ref2);
                    async move {
                        let response = data_ref
                            .lock
                            .write()
                            .await
                            .set_data(&data_file_path, value["value"].to_string())
                            .await;

                        Ok::<warp::reply::Json, warp::Rejection>(warp::reply::json(&response))
                    }
                },
            ))
        .or(warp::path!(String)
            .and(warp::delete())
            .and_then(move |data_file_path: String| {
                let data_ref = Arc::clone(&data_ref3);
                async move {
                    let mut data = data_ref.lock.write().await;
                    let response = data.delete_data(&data_file_path).await;
                    Ok::<warp::reply::Json, warp::Rejection>(warp::reply::json(&response))
                }
            }));

    warp::serve(routes).run(([127, 0, 0, 1], 3001)).await;
}
