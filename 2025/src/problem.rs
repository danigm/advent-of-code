use std::fs::File;
use std::io::prelude::*;

#[derive(Debug)]
pub struct Problem {
    pub day: i32,
    pub input: Option<String>,
}

impl Problem {
    pub fn new(day: i32) -> Self {
        Problem { day: day, input: None }
    }

    pub fn parse_input(&mut self) -> std::io::Result<()> {
        let day = self.day;
        let mut file = File::open(format!("input/{day:02}.data"))?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;

        self.input = Some(contents);

        Ok(())
    }
}
