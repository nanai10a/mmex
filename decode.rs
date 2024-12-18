#![feature(array_chunks)]
#![feature(slice_as_array)]
#![feature(stmt_expr_attributes)]

fn main() {
    let path = get_path();
    let bytes = read_file(&path);
    let matrix = decode_matrix(&*bytes);

    eprintln!("Beginning to write out as CSV...");

    {
        print!("x,y");

        for i in 0..matrix.i {
            for j in 0..matrix.j {
                print!(",m{i}{j}");
            }
        }

        println!();
    }

    for y in 0..matrix.y {
        for x in 0..matrix.x {
            // 上下と左右を反転している
            print!("{x},{y}", x = y, y = x);

            for i in 0..matrix.i {
                for j in 0..matrix.j {
                    // FIXME: 精度は果たしてこれで良いのか
                    print!(",{:+.2}", matrix[(x, y, i, j)]);
                }
            }

            println!();
        }
    }

    eprintln!("Completed to write");
}

fn get_path() -> std::path::PathBuf {
    let args = std::env::args().collect::<Vec<_>>();

    if let Some([executable]) = args.as_array::<1>() {
        eprintln!("Usage: {executable} <path>");
        std::process::exit(1);
    }

    if let Some([_, path]) = args.as_array::<2>() {
        match path.parse() {
            Ok(buf) => return buf,
            Err(err) => {
                eprintln!("Got invalid path: {err}");
                std::process::exit(1);
            }
        }
    }

    let [executable] = args.as_slice() else {
        unreachable!();
    };

    eprintln!("Usage: {executable} <path>");
    std::process::exit(1);
}

fn read_file(path: impl AsRef<std::path::Path>) -> Vec<u8> {
    eprintln!("Reading file: {}", path.as_ref().display());

    match std::fs::read(path) {
        Ok(bytes) => bytes,
        Err(err) => {
            eprintln!("Failed to read file: {err}");
            std::process::exit(1);
        }
    }
}

fn decode_matrix(bytes: &[u8]) -> Matrix {
    if bytes.len() < 16 {
        eprintln!("Cannot decode matrix: no header");
        std::process::exit(1);
    }

    let [x, y, i, j] = bytes[0..16]
        .array_chunks()
        .copied()
        .map(i32::from_be_bytes)
        .collect::<Vec<_>>()
        .as_array()
        .unwrap()
        .map(|num| match usize::try_from(num) {
            Ok(num) => num,
            Err(err) => {
                eprintln!("Cannot decode matrix: Invalid value: {err}");
                std::process::exit(1);
            }
        });

    eprintln!("Found header: shape ({x}, {y}, {i}, {j})");

    let body = &bytes[16..];
    if body.len() != x * y * i * j * std::mem::size_of::<f64>() {
        eprintln!("Cannot decode matrix: invalid body size");
        std::process::exit(1);
    }

    let numbers = body
        .array_chunks()
        .copied()
        .map(f64::from_be_bytes)
        .collect::<Vec<_>>();

    assert_eq!(x * y * i * j, numbers.len());
    eprintln!("Decoded body: {} items", numbers.len());

    #[rustfmt::skip]
    Matrix { numbers, x, y, i, j }
}

struct Matrix {
    numbers: Vec<f64>,

    x: usize,
    y: usize,
    i: usize,
    j: usize,
}

impl std::ops::Index<(usize, usize, usize, usize)> for Matrix {
    type Output = f64;

    fn index(&self, (x, y, i, j): (usize, usize, usize, usize)) -> &Self::Output {
        assert!(x < self.x, "Index out of range in matrix: x = {x}");
        assert!(y < self.y, "Index out of range in matrix: y = {y}");
        assert!(i < self.i, "Index out of range in matrix: i = {i}");
        assert!(j < self.j, "Index out of range in matrix: j = {j}");

        let index = (x * self.y * self.i * self.j) + (y * self.i * self.j) + (i * self.j) + j;
        &self.numbers[index]
    }
}
