import re


def getReviewGrade(reviewGrade):
    goodsGrade = "d"
    if reviewGrade.find("span", class_="rec_a"):
        goodsGrade = "a"
    elif reviewGrade.find("span", class_="rec_b"):
        goodsGrade = "b"
    elif reviewGrade.find("span", class_="rec_c"):
        goodsGrade = "c"
    elif reviewGrade.find("span", class_="rec_d"):
        goodsGrade = "d"

    deliveryGrade = "d"
    if reviewGrade.find("span", class_="dev_a"):
        deliveryGrade = "a"
    elif reviewGrade.find("span", class_="dev_b"):
        deliveryGrade = "b"
    elif reviewGrade.find("span", class_="dev_c"):
        deliveryGrade = "c"
    elif reviewGrade.find("span", class_="dev_d"):
        deliveryGrade = "d"

    return {"goodsGrade": goodsGrade,
            "deliveryGrade": deliveryGrade}


def getItemInfoString(s):
    if s is None:
        return None
    if s == "상세설명참고" or s == "상세페이지참조":
        return None
    s = s.replace(",", " ")
    s = re.sub("\(.*\)", "", s)
    return s


def makeDir(path):
    import os
    path = path.strip()
    path=path.rstrip("\\")

    try:
        os.makedirs(path)
        return True
    except:
        return False

