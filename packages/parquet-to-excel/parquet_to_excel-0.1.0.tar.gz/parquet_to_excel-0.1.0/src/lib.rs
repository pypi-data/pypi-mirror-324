pub mod utils;

use utils::{file_to_xlsx, folder_to_xlsx};
use pyo3::{exceptions::PyException, prelude::{pyfunction, pymodule, wrap_pyfunction, Bound, PyModule, PyModuleMethods as _, PyResult}};


#[pyfunction]
fn parquet_file_to_xlsx(source: String, destination: String, sheet_name: String, sheet_column: String) -> PyResult<()> {
    let sheet_name = if sheet_name.len() ==0 {None} else {Some(sheet_name)};
    let sheet_column = if sheet_column.len() ==0 {None} else {Some(sheet_column)};
    match file_to_xlsx(source, destination, sheet_name, sheet_column) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


#[pyfunction]
fn parquet_files_to_xlsx(source: String, destination: String, sheet_name: String, sheet_column: String) -> PyResult<()> {
    let sheet_name = if sheet_name.len() ==0 {None} else {Some(sheet_name)};
    let sheet_column = if sheet_column.len() ==0 {None} else {Some(sheet_column)};
    match folder_to_xlsx(source, destination, sheet_name, sheet_column) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}




/// A Python module implemented in Rust.
#[pymodule]
fn parquet_to_excel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parquet_file_to_xlsx, m)?)?;
    m.add_function(wrap_pyfunction!(parquet_files_to_xlsx, m)?)?;
    Ok(())
}
