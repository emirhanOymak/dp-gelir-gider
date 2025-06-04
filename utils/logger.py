import logging

logging.basicConfig(
    filename="hata_kayitlari.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message, exception):
    logging.error(f"{message}: {exception}")
