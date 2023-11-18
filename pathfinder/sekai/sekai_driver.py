from .sekai_extractor import SekaiAssetExtractor
def gatcha_card_extract_driver():
    """Driver function to extract and download gatcha card items."""
    extractor = SekaiAssetExtractor(r"E:\sekai\gatcha_card")
    extractor.run_extraction("character/member/")


if __name__ == "__main__":
    gatcha_card_extract_driver()
