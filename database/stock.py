from odmantic import Model


class StockModel(Model):
    
    기업명 : str
    매출액: float
    순이익: float
    구주매출: float
    희망공모가최저: float
    희망공모가최고: float
    청약경쟁률: float
    확정공모가: float
    경쟁률: float
    의무보유확약: int
    공모가: int
    시초가: int
    
    class Config:
        collection = "inform"