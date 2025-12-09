use std::env;
use std::process::ExitCode;

mod problem;
mod problems;

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!("Usage: {} day", args[0]);
        return ExitCode::from(0);
    }

    let arg = &args[1];
    let day: i32 = match arg.parse() {
        Ok(n) => n,
        Err(_) => {
            eprintln!("error: day should be an integer");
            eprintln!("Usage: {} day", args[0]);
            return ExitCode::from(1);
        },
    };

    let mut p = problem::Problem::new(day);
    if let Err(_) = p.parse_input() {
        eprintln!("error parsing {day} input");
        return ExitCode::from(2);
    }

    match day {
        1 => problems::p1::solve(&p),
        _ => println!("Not implemented yet"),
    }

    ExitCode::from(0)
}
