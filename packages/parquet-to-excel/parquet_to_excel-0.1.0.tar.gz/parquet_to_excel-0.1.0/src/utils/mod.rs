
use std::{collections::HashSet, fs::File};
use chrono::DateTime;
use parquet::file::reader::{FileReader, SerializedFileReader};
use xlsx_batch_reader::{write::XlsxWriter, read::IntoCellValue, CellValue};

/// 将parquet文件写入excel文件
pub fn file_to_xlsx<T: AsRef<std::path::Path>>(source: T, destination: T, sheet_name: Option<String>, sheet_column: Option<String>) -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open(source)?;
    let mut book = XlsxWriter::new();
    let mut used = HashSet::new();
    let mut header = Vec::new();
    let sheet_name = if let Some(sheet_name) = &sheet_name {Some(sheet_name)} else {None};
    let sheet_column = if let Some(sheet_column) = &sheet_column {Some(sheet_column)} else {None};
    match do_parquet_to_xlsx(file, &mut book, &mut used, sheet_name, sheet_column, &mut header) {
        Ok(_) => {
            book.save_as(destination)?;
            Ok(())
        },
        Err(e) => {
            Err(e) 
        }
    }
}

/// 将parquet文件夹写入excel文件
pub fn folder_to_xlsx<T: AsRef<std::path::Path>>(source: T, destination: T, sheet_name: Option<String>, sheet_column: Option<String>) -> Result<(), Box<dyn std::error::Error>> {
    fn find_parquet_files<P: AsRef<std::path::Path>>(root: P, book: &mut XlsxWriter, sheet_used: &mut HashSet<String>, sheet_name: Option<&String>, sheet_column: Option<&String>, sheet_headers: &mut Vec<String>) -> Result<(), Box<dyn std::error::Error>> {    
        if let Ok(entries) = std::fs::read_dir(root) {
            for entry in entries {
                if let Ok(entry) = entry {
                    let path = entry.path();
                    if path.is_dir() {
                        find_parquet_files(&path, book, sheet_used, sheet_name, sheet_column, sheet_headers)?;
                    } else if path.is_file() {
                        if let Some(ext) = path.extension() {
                            if ext == "parquet" {
                                let file = File::open(&path)?;
                                do_parquet_to_xlsx(file, book, sheet_used, sheet_name, sheet_column, sheet_headers)?;
                            }
                        }
                    }
                }
            }
        };
        Ok(())
    }
    
    let mut book = XlsxWriter::new();
    let mut used = HashSet::new();
    let mut header = Vec::new();
    let sheet_name = if let Some(sheet_name) = &sheet_name {Some(sheet_name)} else {None};
    let sheet_column = if let Some(sheet_column) = &sheet_column {Some(sheet_column)} else {None};
    match find_parquet_files(source, &mut book, &mut used, sheet_name, sheet_column, &mut header) {
        Ok(_) => {
            book.save_as(destination)?;
            Ok(())
        },
        Err(e) => {
            Err(e)
        }
    }
}

/// 将parquet文件写入excel文件
fn do_parquet_to_xlsx(file: File, book: &mut XlsxWriter, sheet_used: &mut HashSet<String>, sheet_name: Option<&String>, sheet_column: Option<&String>, sheet_headers: &mut Vec<String>) -> Result<(), Box<dyn std::error::Error>> {
    // let file = File::open(path)?;
    // let builder = ParquetRecordBatchReaderBuilder::try_new(file)?;
    // println!("Converted arrow schema is: {}", builder.schema());
    let reader = SerializedFileReader::new(file)?;

    let empty: Vec<u8> = vec![];
    if sheet_headers.is_empty() {
        let schema = reader.metadata().file_metadata().schema_descr();
        for col in schema
            .columns()
            .iter()
            .map(|column| column.name().to_string()) {
            sheet_headers.push(col);
        };
    };
    if sheet_column.is_none() {
        if let Some(sheet_name) = sheet_name {
            if !sheet_used.contains(sheet_name) {
                book.append_row(sheet_name, None, sheet_headers.clone(), &empty)?;
                sheet_used.insert(sheet_name.to_owned());
            }
        }
    }

    match reader.get_row_iter(None) {
        Ok(mut riter) => {
            while let Some(row) = riter.next() {
                match row {
                    Ok(row) => {
                        let mut sheet = String::new();
                        let mut cells = vec![];
                        for (name, field) in row.get_column_iter() {
                            match field {
                                parquet::record::Field::Null => {
                                    cells.push(CellValue::Blank);
                                },
                                parquet::record::Field::Bool(v) => {
                                    cells.push(CellValue::Bool(*v));
                                },
                                parquet::record::Field::Byte(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::Short(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::Int(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::Long(v) => {
                                    cells.push(CellValue::Number((*v) as f64));
                                },
                                parquet::record::Field::UByte(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::UShort(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::UInt(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::ULong(v) => {
                                    cells.push(CellValue::Number((*v) as f64));
                                },
                                parquet::record::Field::Float16(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::Float(v) => {
                                    cells.push(CellValue::Number((*v).into()));
                                },
                                parquet::record::Field::Double(v) => {
                                    cells.push(CellValue::Number(*v));
                                },
                                parquet::record::Field::Decimal(_) => {
                                    cells.push(CellValue::String("不支持的格式-Decimal".into()));
                                },
                                parquet::record::Field::Str(v) => {
                                    cells.push(CellValue::String(v.into()));
                                },
                                parquet::record::Field::Bytes(v) => {
                                    match v.as_utf8() {
                                        Ok(v) => {
                                            cells.push(CellValue::String(v.into()));
                                        },
                                        Err(_) => {
                                            cells.push(CellValue::String("不支持的格式-Bytes".into()));
                                        }
                                    };
                                },
                                parquet::record::Field::Date(v) => {
                                    cells.push(v.try_into_cval()?);
                                },
                                parquet::record::Field::TimestampMillis(v) => {
                                    let dtm = DateTime::from_timestamp_millis(*v).ok_or("时间戳转换异常{v}")?;
                                    cells.push(dtm.naive_local().try_into_cval()?);
                                },
                                parquet::record::Field::TimestampMicros(v) => {
                                    let dtm = DateTime::from_timestamp_micros(*v).ok_or("时间戳转换异常{v}")?;
                                    cells.push(dtm.naive_local().try_into_cval()?);
                                },
                                parquet::record::Field::Group(_) => {
                                    cells.push(CellValue::String("不支持的格式-Group".into()));
                                },
                                parquet::record::Field::ListInternal(_) => {
                                    cells.push(CellValue::String("不支持的格式-ListInternal".into()));
                                },
                                parquet::record::Field::MapInternal(_) => {
                                    cells.push(CellValue::String("不支持的格式-MapInternal".into()));
                                },
                            }
                            if sheet_column == Some(name) {
                                if let Some(s) = cells[cells.len()-1].get::<String>()? {
                                    sheet = s;
                                    if !sheet_used.contains(&sheet) {
                                        book.append_row(&sheet, None, sheet_headers.clone(), &empty)?;
                                        sheet_used.insert(sheet.clone());
                                    };
                                };
                            }
                        }
                        if let Some(sheet_column) = sheet_column  {
                            if sheet.len() > 0 {
                                book.append_row(&sheet, None, cells, &empty)?;
                            } else {
                                book.append_row(sheet_column, None, cells, &empty)?;
                            }
                        } else if let Some(sheet_name) = sheet_name {
                            book.append_row(sheet_name, None, cells, &empty)?;
                        } else {
                            return Err("sheet_name and sheet_column can't both be blank".into());
                        }
                    },
                    Err(e) => {
                        return Err(format!("读取文件出错：{:?}", e).into());
                    },
                }
            }
        },
        Err(_) => {
            return Err(format!("文件不是parquet文件").into())
        },
    }
    Ok(())
}