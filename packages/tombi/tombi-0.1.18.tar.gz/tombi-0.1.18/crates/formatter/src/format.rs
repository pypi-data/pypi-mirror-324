mod array_of_tables;
mod comment;
mod key;
mod key_value;
mod root;
mod table;
mod value;

pub trait Format {
    fn fmt(&self, f: &mut crate::Formatter) -> Result<(), std::fmt::Error>;
}
