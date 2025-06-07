import logging

# Genel log ayarları (hata_kayitlari.log)
logging.basicConfig(
    filename="hata_kayitlari.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(message, exception):
    logging.error(f"{message}: {exception}")

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

# Excel içe aktarım logları (import_log.log)
import_import_logger = logging.getLogger("import_log")
import_handler = logging.FileHandler("import_log.log", encoding="utf-8")
import_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
import_import_logger.setLevel(logging.INFO)
import_import_logger.addHandler(import_handler)

def log_import(message):
    import_import_logger.info(message)
