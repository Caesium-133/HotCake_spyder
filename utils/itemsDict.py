itemReviewInfo = {              ###几乎整合到了ITEM SUMMERY中
    "goodsCode": None,          #商品编码
    "totalCount": None,         #评论总数
    "premiumReviewNum": None,   #优质用户的评论数
    "commonReviewNum": None     #普通用户的评论数
}

premiumReview = {               ###每天爬取一次
    'goodsCode': None,
    'reviewTitle': None,        #评论标题
    'reviewGoodsChoice': None,  #评论商品选项
    'reviewContent': None,      #评论内容
    'reviewerName': None,       #评论用户名
    'reviewDate': None,         #评论日期
    'reviewerExp': None         #评论者已经发表过的评论数量
}

commonReview = {                ###每天爬取一次
    'goodsCode': None,
    'goodsGrade': None,         #对商品的评分abcd
    'deliveryGrade': None,      #对邮递的评分abcd
    'reviewGoodsChoice': None,  #评论商品选项
    'reviewContent': None,      #评论内容
    'reviewerName': None,       #评论者用户名
    'reviewDate': None          #评论日期
}

itemInfoDict = {                ###每7天更新一次
    'goodsCode': None,
    'title': None,              #商品名
    'cat_0': None,              #商品根类别（一般都是home, 无效）
    'cat_1': None,              #商品第一类别
    'cat_1_code':None,          #第一类别编号
    'cat_2': None,              #商品第二类别
    'cat_2_code':None,
    'cat_3': None,
    'cat_3_code':None,
    'cat_4': None,
    'cat_4_code':None,
    'isBest': None,             #是否是"best"商品
    'isOfficial': None,         #是否是"official"商品
    'isSmileDelivery':None,     #是否是"SmileDelivery"商品
    'isExpressShop':None,       #是否是"ExpressShop"商品
    'isSoldOut': None,          #是否售罄
    'realPrice': None,          #真实价格（现价）
    'originalPrice': None,      #原始价格
    'coupon': None,             #优惠券优惠值 如15%或2000韩元
    'shopTitle': None,          #店名
    'isPowerDealer': None,      #店铺是否是"power dealer"
    'isInterestShop': None,     #店铺是否是"interest shop"
    'productStatus': None,      #产品状态 新产品还是二手还是啥
    'businessClassification': None, #业务分类
    'brand': None,              #品牌
    'source': None,             #产地
    'productAndModelName': None,#产品和型号
    'ManufacturerNImporter': None,  #制造商和进口商
    'countryOfManufacture':None,#生产国
    'bookName':None,            #书名/专辑名
    'author':None,              #作者
    'publisher':None,           #出版商
    'material':None,
    'size':None,                #大小 20mmx30mm
    'width':None,               #kuandu
    'weight':None,              #zhongliang
    'colour':None,              #颜色
    'updateDate':None           #本信息更新时间
}

itemInfoSummaryDict={               ###每小时爬取一次
    'goodsCode':None,
    'price':None,
    'coupon':None,
    'reviewsNum':None,
    'premiumReviewsNum':None,
    'commonReviewsNum':None,
    'isSoldOut':None
}
