# utils/logger.py

import logging

# Log yapılandırması
logging.basicConfig(
    filename="hata_kayitlari.log",
    level=logging.INFO,  # Artık INFO seviyesinden itibaren tüm loglar alınacak
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message, exception):
    logging.error(f"{message}: {exception}")

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)
