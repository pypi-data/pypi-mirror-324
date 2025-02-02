use dim_rs::{prelude::*, vectorization::ModelParameters};
use image::DynamicImage;
use pyo3::prelude::*;
use async_openai;
use pyo3_asyncio::tokio::{future_into_py_with_locals, get_current_locals};

/// Vectorizes a text string using concurrent processing
/// 
/// Args:
///     py: Python interpreter instance
///     string: The input text to vectorize
///     prompts: List of prompts to use for vectorization
///     api_key: API key
///     model: Name of the model to use
///     temperature: Optional temperature setting for the model
///     seed: Optional seed for random number generation
///     base_url: Optional custom API base URL
///
/// Returns:
///     Vector of floats representing the vectorized text
#[pyfunction]
pub fn vectorize_string(
    py: Python,
    string: String,
    prompts: Vec<String>,
    api_key: String,
    model: String,
    temperature: Option<f32>,
    seed: Option<i64>,
    base_url: Option<String>,
) -> PyResult<&PyAny> {
    let mut rust_vector: Vector<String> = Vector::from_text(string);
    let client = async_openai::Client::with_config(
        async_openai::config::OpenAIConfig::new()
            .with_api_key(api_key)
            .with_api_base(base_url.unwrap_or("https://api.openai.com".to_string()))
    );

    future_into_py_with_locals(
        py, 
        get_current_locals(py)?,
        async move {
            let model_params = ModelParameters::new(model, temperature, seed);
            match vectorize_string_concurrently(prompts, &mut rust_vector, client, model_params).await {
                Ok(_) => Ok(rust_vector.get_vector()),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
            }
        }
    )
}

/// Vectorizes an image using concurrent processing
///
/// Args:
///     py: Python interpreter instance
///     image_bytes: Raw bytes of the image to vectorize
///     prompts: List of prompts to use for vectorization 
///     model: Name of the OpenAI model to use
///     api_key: OpenAI API key
///     temperature: Optional temperature setting for the model
///     seed: Optional seed for random number generation
///     base_url: Optional custom API base URL
///
/// Returns:
///     Vector of floats representing the vectorized image
#[pyfunction]
pub fn vectorize_image(
    py: Python,
    image_bytes: Vec<u8>,
    prompts: Vec<String>, 
    model: String,
    api_key: String,
    temperature: Option<f32>,
    seed: Option<i64>,
    base_url: Option<String>,
) -> PyResult<&PyAny> {
    let image = image::load_from_memory(&image_bytes)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

    let mut rust_vector: Vector<DynamicImage> = Vector::from_image(image);
    let client = async_openai::Client::with_config(
        async_openai::config::OpenAIConfig::new()
            .with_api_key(api_key)
            .with_api_base(base_url.unwrap_or("https://api.openai.com".to_string()))
    );

    future_into_py_with_locals(
        py,
        get_current_locals(py)?,
        async move {
            let model_params = ModelParameters::new(model, temperature, seed);
            match vectorize_image_concurrently(prompts, &mut rust_vector, client, model_params).await {
                Ok(_) => Ok(rust_vector.get_vector()),
                Err(e) => Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))
            }
        }
    )
}