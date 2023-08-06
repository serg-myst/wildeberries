import json
import xlsxwriter

requisites = {
    'realizationreport_id': 'Номер отчёта',
    'date_from': 'Дата начала отчётного периода',
    'date_to': 'Дата конца отчётного периода',
    'create_dt': 'Дата формирования отчёта',
    'currency_name': 'Валюта отчёта',
    'suppliercontract_code': 'Договор',
    'rrd_id': 'Номер строки',
    'gi_id': 'Номер поставки',
    'subject_name': 'Предмет',
    'nm_id': 'Артикул WB',
    'brand_name': 'Бренд',
    'sa_name': 'Артикул продавца',
    'ts_name': 'Размер',
    'barcode': 'Баркод',
    'doc_type_name': 'Тип документа',
    'quantity': 'Количество',
    'retail_price': 'Цена розничная',
    'retail_amount': 'Сумма продаж (возвратов)',
    'sale_percent': 'Согласованная скидка',
    'commission_percent': 'Процент комиссии',
    'office_name': 'Склад',
    'supplier_oper_name': 'Обоснование для оплаты',
    'order_dt': 'Дата заказа',
    'sale_dt': 'Дата продажи',
    'rr_dt': 'Дата операции',
    'shk_id': 'Штрих-код',
    'retail_price_withdisc_rub': 'Цена розничная с учетом согласованной скидки',
    'delivery_amount': 'Количество доставок',
    'return_amount': 'Количество возвратов',
    'delivery_rub': 'Стоимость логистики',
    'gi_box_type_name': 'Тип коробов',
    'product_discount_for_report': 'Согласованный продуктовый дисконт',
    'supplier_promo': 'Промокод',
    'rid': 'Уникальный идентификатор заказа',
    'ppvz_spp_prc': 'Скидка постоянного покупателя',
    'ppvz_kvw_prc_base': 'Размер кВВ без НДС, % базовый',
    'ppvz_kvw_prc': 'Итоговый кВВ без НДС, %',
    'sup_rating_prc_up': 'Размер снижения кВВ из-за рейтинга',
    'is_kgvp_v2': 'Размер снижения кВВ из-за акции',
    'ppvz_sales_commission': 'Вознаграждение с продаж до вычета услуг поверенного, без НДС',
    'ppvz_for_pay': 'К перечислению продавцу за реализованный товар',
    'ppvz_reward': 'Возмещение за выдачу и возврат товаров на ПВЗ',
    'acquiring_fee': 'Возмещение издержек по эквайрингу',
    'acquiring_bank': 'Наименование банка-эквайера',
    'ppvz_vw': 'Вознаграждение WB без НДС',
    'ppvz_vw_nds': 'НДС с вознаграждения WB',
    'ppvz_office_id': 'Номер офиса',
    'ppvz_office_name': 'Наименование офиса доставки',
    'ppvz_supplier_id': 'Номер партнера',
    'ppvz_supplier_name': 'Партнер',
    'ppvz_inn': 'ИНН партнера',
    'declaration_number': 'Номер таможенной декларации',
    'bonus_type_name': 'Обоснование штрафов и доплат',
    'sticker_id': 'Цифровое значение стикера, который клеится на товар в процессе сборки заказа по схеме "Маркетплейс"',
    'site_country': 'Страна продажи',
    'penalty': 'Штрафы',
    'additional_payment': 'Доплаты',
    'rebill_logistic_cost': 'Возмещение издержек по перевозке. Поле будет в ответе при наличии значения',
    'rebill_logistic_org': 'Организатор перевозки. Поле будет в ответе при наличии значения',
    'kiz': 'Код маркировки',
    'srid': 'Уникальный идентификатор заказа. Примечание для использующих API Marketplace'
}


def create_xls():
    with xlsxwriter.Workbook(f'report_csv.csv') as f:
        worksheet = f.add_worksheet()
        i = 0
        for value in requisites.values():
            worksheet.write(0, i, value)
            i += 1
        with open('response_1690877085693.json', 'r', encoding='utf-8') as f:
            reports = json.load(f)
            i = 1
            for report in reports:
                j = 0
                for key in requisites.keys():
                    worksheet.write(i, j, report.get(key))
                    j += 1
                i += 1


if __name__ == '__main__':
    create_xls()
