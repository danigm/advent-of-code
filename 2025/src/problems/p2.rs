use std::str::FromStr;

use crate::problem;

// Invalid are silly patterns
// Sequence of digits repeated twice
fn is_invalid(id: &str) -> bool {
    let bytes = id.as_bytes();
    let l = bytes.len();
    if l % 2 != 0 {
        return false;
    }

    let n = l / 2;
    for i in 0..n {
        let n1 = n+i;
        if bytes[i] != bytes[n1] {
            return false;
        }
    }

    return true;
}

// Invalid are repeaded sequences
fn is_invalid2(id: &str) -> bool {
    let bytes = id.as_bytes();
    let l = bytes.len();

    for i in 2..l/2+1 {
        let parts = i;

        let n = l / parts;
        for j in 0..n {
            let mut valid = false;
            for k in 1..parts {
                let n1 = (n * k) +j;
                if bytes[j] != bytes[n1] {
                    valid = true;
                    break;
                }
                if n1 == l - 1 {
                    return true;
                }
            }
            if valid {
                break;
            }
        }
    }

    for i in bytes {
        if i != &bytes[0] {
            return false;
        }
    }

    return true;
}

fn count_invalids2(a: u64, b: u64) -> u64 {
    let mut n = 0;
    for i in a..b+1 {
        if is_invalid2(&format!("{i}")) {
            n += i;
        }
    }
    n
}

fn transform_data(d: &String) -> Vec<(u64, u64)> {
    let mut ranges = vec![];
    for line in d.lines() {
        for range in line.split(",") {
            if range == "" {
                continue;
            }
            let v: Vec<&str> = range.split("-").collect();
            let a = u64::from_str(v[0]).expect("wrong number");
            let b = u64::from_str(v[1]).expect("wrong number");
            ranges.push((a, b));
        }
    }

    ranges
}

fn count_invalids(a: u64, b: u64) -> u64 {
    let mut n = 0;
    for i in a..b+1 {
        if is_invalid(&format!("{i}")) {
            n += i;
        }
    }
    n
}

fn add_invalids(d: &Vec<(u64, u64)>) -> u64 {
    let mut n = 0;
    for (a, b) in d {
        n += count_invalids(*a, *b);
    }
    n
}

fn add_invalids2(d: &Vec<(u64, u64)>) -> u64 {
    let mut n = 0;
    for (a, b) in d {
        n += count_invalids2(*a, *b);
    }
    n
}

pub fn solve(p: &problem::Problem) {
    println!("Day two: Gift Shop");

    let input = p.input.as_ref().unwrap();
    let data = transform_data(input);

    let p1 = add_invalids(&data);
    println!("puzzle 1: {p1}");
    let p2 = add_invalids2(&data);
    println!("puzzle 2: {p2}");
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn p1_test() {
        let input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124";

        assert!(!is_invalid("12"));
        assert!(!is_invalid("1234"));

        assert!(is_invalid("11"));
        assert!(is_invalid("22"));
        assert!(is_invalid("1188511885"));

        assert_eq!(count_invalids(11, 22), 33);
        assert_eq!(count_invalids(95, 115), 99);
        assert_eq!(count_invalids(998, 1012), 1010);

        assert_eq!(add_invalids(&transform_data(&String::from(input))), 1227775554);
    }

    #[test]
    fn p2_test() {
        let input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124";

        assert!(!is_invalid2("12"));
        assert!(is_invalid2("11"));
        assert!(is_invalid2("22"));
        assert!(is_invalid2("1188511885"));
        assert!(is_invalid2("824824824"));

        assert!(is_invalid2("1010"));
        assert_eq!(count_invalids2(998, 1012), 999 + 1010);
        assert_eq!(count_invalids2(824824821, 824824827), 824824824);
        assert_eq!(add_invalids2(&transform_data(&String::from(input))), 4174379265);
    }
}
