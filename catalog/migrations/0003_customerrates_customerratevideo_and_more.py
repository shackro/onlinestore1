# Generated by Django 5.1.4 on 2025-02-08 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_address_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrates',
            name='customerratevideo',
            field=models.FileField(blank=True, null=True, upload_to='customerrate/videos/'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='country_code',
            field=models.CharField(choices=[('+1', 'AG (+1)'), ('+1', 'AI (+1)'), ('+1', 'AS (+1)'), ('+1', 'BB (+1)'), ('+1', 'BM (+1)'), ('+1', 'BS (+1)'), ('+1', 'CA (+1)'), ('+1', 'DM (+1)'), ('+1', 'DO (+1)'), ('+1', 'GD (+1)'), ('+1', 'GU (+1)'), ('+1', 'JM (+1)'), ('+1', 'KN (+1)'), ('+1', 'KY (+1)'), ('+1', 'LC (+1)'), ('+1', 'MP (+1)'), ('+1', 'MS (+1)'), ('+1', 'PR (+1)'), ('+1', 'SX (+1)'), ('+1', 'TC (+1)'), ('+1', 'TT (+1)'), ('+1', 'US (+1)'), ('+1', 'VC (+1)'), ('+1', 'VG (+1)'), ('+1', 'VI (+1)'), ('+20', 'EG (+20)'), ('+211', 'SS (+211)'), ('+212', 'EH (+212)'), ('+212', 'MA (+212)'), ('+213', 'DZ (+213)'), ('+216', 'TN (+216)'), ('+218', 'LY (+218)'), ('+220', 'GM (+220)'), ('+221', 'SN (+221)'), ('+222', 'MR (+222)'), ('+223', 'ML (+223)'), ('+224', 'GN (+224)'), ('+225', 'CI (+225)'), ('+226', 'BF (+226)'), ('+227', 'NE (+227)'), ('+228', 'TG (+228)'), ('+229', 'BJ (+229)'), ('+230', 'MU (+230)'), ('+231', 'LR (+231)'), ('+232', 'SL (+232)'), ('+233', 'GH (+233)'), ('+234', 'NG (+234)'), ('+235', 'TD (+235)'), ('+236', 'CF (+236)'), ('+237', 'CM (+237)'), ('+238', 'CV (+238)'), ('+239', 'ST (+239)'), ('+240', 'GQ (+240)'), ('+241', 'GA (+241)'), ('+242', 'CG (+242)'), ('+243', 'CD (+243)'), ('+244', 'AO (+244)'), ('+245', 'GW (+245)'), ('+246', 'IO (+246)'), ('+247', 'AC (+247)'), ('+248', 'SC (+248)'), ('+249', 'SD (+249)'), ('+250', 'RW (+250)'), ('+251', 'ET (+251)'), ('+252', 'SO (+252)'), ('+253', 'DJ (+253)'), ('+254', 'KE (+254)'), ('+255', 'TZ (+255)'), ('+256', 'UG (+256)'), ('+257', 'BI (+257)'), ('+258', 'MZ (+258)'), ('+260', 'ZM (+260)'), ('+261', 'MG (+261)'), ('+262', 'RE (+262)'), ('+262', 'YT (+262)'), ('+263', 'ZW (+263)'), ('+264', 'NA (+264)'), ('+265', 'MW (+265)'), ('+266', 'LS (+266)'), ('+267', 'BW (+267)'), ('+268', 'SZ (+268)'), ('+269', 'KM (+269)'), ('+27', 'ZA (+27)'), ('+290', 'SH (+290)'), ('+290', 'TA (+290)'), ('+291', 'ER (+291)'), ('+297', 'AW (+297)'), ('+298', 'FO (+298)'), ('+299', 'GL (+299)'), ('+30', 'GR (+30)'), ('+31', 'NL (+31)'), ('+32', 'BE (+32)'), ('+33', 'FR (+33)'), ('+34', 'ES (+34)'), ('+350', 'GI (+350)'), ('+351', 'PT (+351)'), ('+352', 'LU (+352)'), ('+353', 'IE (+353)'), ('+354', 'IS (+354)'), ('+355', 'AL (+355)'), ('+356', 'MT (+356)'), ('+357', 'CY (+357)'), ('+358', 'AX (+358)'), ('+358', 'FI (+358)'), ('+359', 'BG (+359)'), ('+36', 'HU (+36)'), ('+370', 'LT (+370)'), ('+371', 'LV (+371)'), ('+372', 'EE (+372)'), ('+373', 'MD (+373)'), ('+374', 'AM (+374)'), ('+375', 'BY (+375)'), ('+376', 'AD (+376)'), ('+377', 'MC (+377)'), ('+378', 'SM (+378)'), ('+380', 'UA (+380)'), ('+381', 'RS (+381)'), ('+382', 'ME (+382)'), ('+383', 'XK (+383)'), ('+385', 'HR (+385)'), ('+386', 'SI (+386)'), ('+387', 'BA (+387)'), ('+389', 'MK (+389)'), ('+39', 'IT (+39)'), ('+39', 'VA (+39)'), ('+40', 'RO (+40)'), ('+41', 'CH (+41)'), ('+420', 'CZ (+420)'), ('+421', 'SK (+421)'), ('+423', 'LI (+423)'), ('+43', 'AT (+43)'), ('+44', 'GB (+44)'), ('+44', 'GG (+44)'), ('+44', 'IM (+44)'), ('+44', 'JE (+44)'), ('+45', 'DK (+45)'), ('+46', 'SE (+46)'), ('+47', 'NO (+47)'), ('+47', 'SJ (+47)'), ('+48', 'PL (+48)'), ('+49', 'DE (+49)'), ('+500', 'FK (+500)'), ('+501', 'BZ (+501)'), ('+502', 'GT (+502)'), ('+503', 'SV (+503)'), ('+504', 'HN (+504)'), ('+505', 'NI (+505)'), ('+506', 'CR (+506)'), ('+507', 'PA (+507)'), ('+508', 'PM (+508)'), ('+509', 'HT (+509)'), ('+51', 'PE (+51)'), ('+52', 'MX (+52)'), ('+53', 'CU (+53)'), ('+54', 'AR (+54)'), ('+55', 'BR (+55)'), ('+56', 'CL (+56)'), ('+57', 'CO (+57)'), ('+58', 'VE (+58)'), ('+590', 'BL (+590)'), ('+590', 'GP (+590)'), ('+590', 'MF (+590)'), ('+591', 'BO (+591)'), ('+592', 'GY (+592)'), ('+593', 'EC (+593)'), ('+594', 'GF (+594)'), ('+595', 'PY (+595)'), ('+596', 'MQ (+596)'), ('+597', 'SR (+597)'), ('+598', 'UY (+598)'), ('+599', 'BQ (+599)'), ('+599', 'CW (+599)'), ('+60', 'MY (+60)'), ('+61', 'AU (+61)'), ('+61', 'CC (+61)'), ('+61', 'CX (+61)'), ('+62', 'ID (+62)'), ('+63', 'PH (+63)'), ('+64', 'NZ (+64)'), ('+65', 'SG (+65)'), ('+66', 'TH (+66)'), ('+670', 'TL (+670)'), ('+672', 'NF (+672)'), ('+673', 'BN (+673)'), ('+674', 'NR (+674)'), ('+675', 'PG (+675)'), ('+676', 'TO (+676)'), ('+677', 'SB (+677)'), ('+678', 'VU (+678)'), ('+679', 'FJ (+679)'), ('+680', 'PW (+680)'), ('+681', 'WF (+681)'), ('+682', 'CK (+682)'), ('+683', 'NU (+683)'), ('+685', 'WS (+685)'), ('+686', 'KI (+686)'), ('+687', 'NC (+687)'), ('+688', 'TV (+688)'), ('+689', 'PF (+689)'), ('+690', 'TK (+690)'), ('+691', 'FM (+691)'), ('+692', 'MH (+692)'), ('+7', 'KZ (+7)'), ('+7', 'RU (+7)'), ('+81', 'JP (+81)'), ('+82', 'KR (+82)'), ('+84', 'VN (+84)'), ('+850', 'KP (+850)'), ('+852', 'HK (+852)'), ('+853', 'MO (+853)'), ('+855', 'KH (+855)'), ('+856', 'LA (+856)'), ('+86', 'CN (+86)'), ('+880', 'BD (+880)'), ('+886', 'TW (+886)'), ('+90', 'TR (+90)'), ('+91', 'IN (+91)'), ('+92', 'PK (+92)'), ('+93', 'AF (+93)'), ('+94', 'LK (+94)'), ('+95', 'MM (+95)'), ('+960', 'MV (+960)'), ('+961', 'LB (+961)'), ('+962', 'JO (+962)'), ('+963', 'SY (+963)'), ('+964', 'IQ (+964)'), ('+965', 'KW (+965)'), ('+966', 'SA (+966)'), ('+967', 'YE (+967)'), ('+968', 'OM (+968)'), ('+970', 'PS (+970)'), ('+971', 'AE (+971)'), ('+972', 'IL (+972)'), ('+973', 'BH (+973)'), ('+974', 'QA (+974)'), ('+975', 'BT (+975)'), ('+976', 'MN (+976)'), ('+977', 'NP (+977)'), ('+98', 'IR (+98)'), ('+992', 'TJ (+992)'), ('+993', 'TM (+993)'), ('+994', 'AZ (+994)'), ('+995', 'GE (+995)'), ('+996', 'KG (+996)'), ('+998', 'UZ (+998)')], default='+44  ', max_length=5),
        ),
    ]
