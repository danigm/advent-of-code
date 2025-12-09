use std::str::FromStr;

use crate::problem;

/// Calculate the combination for the lock
/// It receives a vec of (direction, n)
/// direction: -1 left, 1 right
/// n: the number of steps
fn p1(initial: i32, max: i32, rotations: Vec<(i32, i32)>) -> (i32, i32) {
    let mut count: i32 = 0;
    let mut total: i32 = 0;

    let mut dial = initial;
    for (d, n) in rotations {
        let prev = dial;
        let full = n / max;
        let rot = n % max;

        total += full;

        dial = dial + (d * rot);
        if prev != 0 && dial < 0 {
            dial = max + dial;
            total += 1;
        }
        if dial >= max {
            if dial > max {
                total += 1;
            }
            dial = dial % max;
        }
        if dial == 0 {
            count += 1;
            if rot != 0 {
                total += 1;
            }
        }
    }
    (count, total)
}

fn transform_data(input: &String) -> Vec<(i32, i32)> {
    let mut r: Vec<(i32, i32)> = vec![];
    for line in input.lines() {
        let (dir, steps) = line.trim().split_at(1);
        let d = match dir { "L" => -1, _ => 1 };
        let n = i32::from_str(steps).unwrap_or(0);
        r.push((d, n));
    }
    r
}

pub fn solve(p: &problem::Problem) {
    println!("P1 solution");

    let s = String::from(String::from(p.input.as_ref().unwrap()).trim());
    let data = transform_data(&s);
    let solution = p1(50, 100, data);
    println!("{}", solution.0);
    println!("{}", solution.1);
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn p1_test() {
        let input = "
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82";

        let s = String::from(String::from(input).trim());
        let data = transform_data(&s);
        assert_eq!((-1, 68), data[0]);
        assert_eq!((1, 48), data[2]);
        assert_eq!((3, 6), p1(50, 100, data));
        assert_eq!((0, 10), p1(50, 100, vec![(1, 1000)]));
        assert_eq!((0, 10), p1(50, 100, vec![(-1, 1000)]));
        assert_eq!((0, 20), p1(50, 100, vec![(1, 1000), (-1, 1000)]));
    }
}
