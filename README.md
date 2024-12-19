# mmex

*Mueller Matrix EXperiments*

---

## Preparing

### Rust

[rustup](https://rustup.rs) の利用を推奨します.

```bash
cargo +nightly build --release
```

### Python

venv の利用を推奨します.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

### `decode`

最後の `mm.bin` は読み込みたいファイルへのパスです.

```bash
cargo +nightly run --bin decode -- mm.bin
```

標準出力に CSV が出力されるので, 概ね次のような用途が想定されています.

```bash
cargo +nightly run --bin decode -- mm.bin > mm.csv
```

これで `mm.csv` に CSV データが書き込まれます.

### `map`

最後の `mm.csv` は読み込みたいファイルへのパスです.

```bash
python3 map.py mm.csv
```

各要素毎の数値分布が表示されます.

### `plot`

最後の `mm.csv` は読み込みたいファイルへのパスです.

```bash
python3 plot.py mm.csv
```

時間が掛かりますが, 暫くすると各成分について X-Y 軸にマップされて表示されます.
