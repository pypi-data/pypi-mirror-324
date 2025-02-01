use pyo3::prelude::*;
use std::collections::HashMap;

#[pyclass]
struct StreamValidator {
    schema: HashMap<String, FieldValidator>,
    batch_size: usize,
}

struct FieldValidator {
    field_type: FieldType,
    required: bool,
}

#[derive(Clone)]
enum FieldType {
    String,
    Integer,
    Float,
    Boolean,
    List(Box<FieldType>),
    Dict(Box<FieldType>),
}

#[pymethods]
impl StreamValidator {
    #[new]
    fn new() -> Self {
        StreamValidator {
            schema: HashMap::new(),
            batch_size: 1000,
        }
    }

    #[getter]
    fn batch_size(&self) -> usize {
        self.batch_size
    }

    fn add_field(&mut self, name: String, field_type: &str, required: bool) -> PyResult<()> {
        let field_type = match field_type {
            "str" => FieldType::String,
            "int" => FieldType::Integer,
            "float" => FieldType::Float,
            "bool" => FieldType::Boolean,
            _ => return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                format!("Unsupported type: {}", field_type)
            )),
        };

        self.schema.insert(name, FieldValidator {
            field_type,
            required,
        });
        Ok(())
    }

    fn set_batch_size(&mut self, size: usize) {
        self.batch_size = size;
    }

    fn validate_batch(&self, items: Vec<&PyAny>) -> PyResult<Vec<bool>> {
        let mut results = Vec::with_capacity(items.len());
        
        for item in items {
            match self.validate_item_internal(item) {
                Ok(_) => results.push(true),
                Err(_) => results.push(false),
            }
        }
        Ok(results)
    }

    fn validate_item_internal(&self, item: &PyAny) -> PyResult<bool> {
        if !item.is_instance_of::<pyo3::types::PyDict>()? {
            return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Item must be a dict"));
        }

        let dict = item.downcast::<pyo3::types::PyDict>()?;
        
        for (field_name, validator) in &self.schema {
            if let Some(value) = dict.get_item(field_name) {
                self.validate_value(value, &validator.field_type)?;
            } else if validator.required {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("Required field {} is missing", field_name)
                ));
            }
        }

        Ok(true)
    }
}

// Private implementation - not exposed to Python
impl StreamValidator {
    fn validate_value(&self, value: &PyAny, field_type: &FieldType) -> PyResult<()> {
        match field_type {
            FieldType::String => {
                if !value.is_instance_of::<pyo3::types::PyString>()? {
                    return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Expected string"));
                }
            }
            FieldType::Integer => {
                if !value.is_instance_of::<pyo3::types::PyInt>()? {
                    return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Expected integer"));
                }
            }
            FieldType::Float => {
                if !value.is_instance_of::<pyo3::types::PyFloat>()? {
                    return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Expected float"));
                }
            }
            FieldType::Boolean => {
                if !value.is_instance_of::<pyo3::types::PyBool>()? {
                    return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>("Expected boolean"));
                }
            }
            _ => {}
        }
        Ok(())
    }
}

#[pymodule]
fn _satya(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StreamValidator>()?;
    Ok(())
}