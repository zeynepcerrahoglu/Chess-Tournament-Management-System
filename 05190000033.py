import math  # Tur sayılarının aralığını bulmak için import etmeliyiz


# Sabitler
PUAN_SIFIR = 0  # Puanlama da kullanılacak olan değeri sıfır olan sabit
PUAN_BIR = 1
MAC_SONUCU_BIR = 1
MAC_SONUCU_IKI = 2
MAC_SONUCU_UC = 3
MAC_SONUCU_DORT = 4
PUAN_SIFIR_NOKTA_BES = 0.5
SIFIR = 0  # Elo ve Ukd puanlarının aralığını kontrol ederken kullanılacak olan değeri sıfır olan sabit
BIN = 1000  # Elo ve Ukd puanlarının aralğını kontrol ederken kullanılacak


# Ana fonksiyondur. Programın çalışması için main fonksiyonu çağırılmalıdır.
def main():
    oyuncu_listesi = []  # Oyuncuların bilgilerini tutacak olan iki boyutlu liste
    oyuncu_dic = {}  # Oyuncuların tur bilgilerini tutacak olan dic. Valuelar iki boyutlu listeler olacaktır
    tur_atla_durumu = []  # Oyuncuların daha önce tur atlama durumlarını tutacak olan tek boyutlu liste
    tur_sayisi, renk = verileri_al(oyuncu_listesi, tur_atla_durumu)
    masa_sayisi = len(oyuncu_listesi) // 2
    tek_kalan_durum = liste_tek_mi_cift_mi(oyuncu_listesi)  # Tek kalan oyuncu olacak mı
    ilk_tur(oyuncu_listesi, tur_atla_durumu, tek_kalan_durum, oyuncu_dic, masa_sayisi, renk)
    maclar(tur_sayisi, oyuncu_listesi, tur_atla_durumu, oyuncu_dic, masa_sayisi, tek_kalan_durum)  # eşleştirme
    esitlik_bozma_olcutleri(oyuncu_listesi, oyuncu_dic)
    nihai_siralama(oyuncu_listesi)
    capraz_tablo(oyuncu_listesi, oyuncu_dic, tur_sayisi)


# Nihai sıralama tablosunu yazar
def nihai_siralama(oyuncu_listesi):

    # Yazdırmadan önce eşitlik bozma kurallarına göre sort işlemi yapmalıyız
    oyuncu_listesi.sort(key=lambda index: (index[5], index[6], index[7], index[8], index[9]), reverse=True)

    # Print işlemleri
    print("\nNihai Sıralama Listesi:")
    print("SNo BSNo LNo   Ad-Soyad      ELO  UKD Puan  BH-1  BH-2   SB  GS")
    print("--- ---- ----- ------------ ---- ---- ---- ----- ----- ----- --")
    sayac = 0  # Sayac değeri for döngüsünün sonunda o oyuncunun sıra numarası olacaktır
    for oyuncu in oyuncu_listesi:  # Listedeki her oyuncu sırasıyla yazdırılır
        sayac += 1
        print(format(sayac, "3"), end=" ")
        print(format(oyuncu[0], "4"), format(oyuncu[1], "5"), oyuncu[2], " " * (12 - len(oyuncu[2])), end="")
        print(format(oyuncu[3], "4"), end=" ")
        print(format(oyuncu[4], "4"), format(oyuncu[5], "4.2f"), format(oyuncu[6], "5.2f"), format(oyuncu[7], "5.2f"), end=" ")
        print(format(oyuncu[8], "5.2f"), format(oyuncu[9], "2"))
        oyuncu.insert(0, sayac)


# En son gelecek olan çıktı çapraz tablodur
def capraz_tablo(oyuncu_listesi, oyuncu_dic, tur_sayisi):

    # Yazdırmadan önce başlangıc sıra numaralarına göre sıralanmalıdırlar
    oyuncu_listesi.sort(key=lambda index: index[1])

    # Print işlemleri
    # Her programda tur sayısı değişeceğinden tabloda bu kısım ayarlanarak yazdırılmalıdır
    print("\nÇapraz Tablo:")
    print("BSNo SNo  LNo    Ad-Soyad   ELO  UKD", end="  ")
    for tur in range(tur_sayisi):
        print("", "{}. Tur".format(tur+1), end=" ")
    print("Puan  BH-1  BH-2   SB  GS")
    print("---- --- ----- ------------ ---- ----", end=" ")
    for tur in range(tur_sayisi):
        print("-------", end=" ")
    print("---- ----- ----- ----- --")

    # Daha sonra oyuncu bilgileri sırasıyla yazdırılır
    # Hem liste hem de turların verilerinin tutuluduğu dic kullanılır
    for oyuncu in oyuncu_listesi:
        print(format(oyuncu[1], "4"), format(oyuncu[0], "3"), format(oyuncu[2], "5"), end=" ")
        print(oyuncu[3], " " * (12 - len(oyuncu[3])), end="")
        print(format(oyuncu[4], "4"), format(oyuncu[5], "4"), end=" ")
        values = oyuncu_dic.get(oyuncu[1])  # O oyuncunun tur bilgileri dic alınır
        for value in values:
            print("", value[0], value[1], value[2], end="  ")
        print(format(oyuncu[6], "4.2f"), format(oyuncu[7], "5.2f"), format(oyuncu[8], "5.2f"), format(oyuncu[9], "5.2f"), end=" ")
        print(format(oyuncu[10], "2"))


# İlk tur ile ilgili işlemler bittikten, oyuncuların puanları verildikten sonra olacak eşleştirmeler bu fonk yapılır
def maclar(tur_sayisi, oyuncu_listesi, tur_atla_durum, oyuncu_dic, masa_sayisi, tek_kalan_durum):

    for tur in range(tur_sayisi-1):  # Tur sayısı kadar dönecek olan bir for döngüsü

        puanlar = {}  # Oyuncuların puanları keyleri, bsno numaraları da value değerlerini oluşturur.
        # Puan gruplarına göre rakip arama adımları bu puan gruplarında yapılır
        beyazlar = []  # Beyaz renk alacakların atanacağı liste daha sonra iki boyutlu olacaktır.
        siyahlar = []  # Siyah renk alacakların atanacağı liste daha sonra iki boyutlu olacaktır
        tek_kalan = []  # BYE geçen oyuncunun bilgilerini bulundurur

        siralama_islemi(oyuncu_listesi)  # Her tur eşleştirmesi işlemi oncesi oyuncu listesi belli koşullara göre sıralanmalıdır.

        # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
        if tek_kalan_durum:
            tek_kalan_al(tur_atla_durum, oyuncu_listesi, tek_kalan)

        puanlar_listesi_olustur(puanlar, oyuncu_listesi)
        eslestirmeler(oyuncu_listesi, beyazlar, siyahlar, puanlar, oyuncu_dic)

        # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
        if tek_kalan_durum:
            oyuncu_listesi.append(tek_kalan[0])

        tur_ciktilari(tur, siyahlar, beyazlar, tek_kalan)
        puan_al(oyuncu_listesi, oyuncu_dic, beyazlar, siyahlar, masa_sayisi, tek_kalan, tur_atla_durum, tek_kalan_durum)


# Eşitlik bozma olcutlerıne göre belirlenecek puanların hesaplandığı ve listeye atandığı fonkdur.
def esitlik_bozma_olcutleri(oyuncu_listesi, oyuncu_dic):

    for oyuncu in oyuncu_listesi:

        rakipler_puan = []  # Rakiplerinin puanlarını toplama işlemlerine tabii tutmak için bu listenin içinde biriktiririz.
        sb = 0
        galibiyet = 0

        galibiyet, sb = rakipler_al(oyuncu_listesi, oyuncu_dic, oyuncu, rakipler_puan, galibiyet, sb)
        listeye_ekle(rakipler_puan, sb, galibiyet, oyuncu)


def listeye_ekle(rakipler_puan, sb, galibiyet, oyuncu):

    rakipler_puan.sort()  # Rakilerin puanlarını listeden alırken kolayca işlem yapabilmemiz için sort etmemiz gerekir
    # Bu sayede en düşük puandan en yüksek puana göre sıralanmış bir liste elde etmiş oluruz

    bh1, bh2 = esitlik_puanlari_al(rakipler_puan)

    # Oyuncu listesinin belli indexlerine puan eklemeleri yapılır
    oyuncu[6] += bh1
    oyuncu[7] += bh2
    oyuncu[8] += sb
    oyuncu[9] += galibiyet


# BH1 BH2 puanlarını rakiplerin puanlarının tutulduğu listeden alacak olan fonk
def esitlik_puanlari_al(rakipler_puan):

    bh1 = sum(rakipler_puan[1:])
    bh2 = sum(rakipler_puan[2:])
    return bh1, bh2


# Rakiplerin puanları listeye eklendiği ve genel istatistiksel işlemlerin yapıldığı fonk
def rakipler_al(oyuncu_listesi, oyuncu_dic, oyuncu, rakipler_puan, galibiyet, sb):

    aldigi_puan = 0  # O tura kadar aldığı puanı tutar
    values = oyuncu_dic.get(oyuncu[0])  # Oyuncu dic den o oyunucun tur bilgileri cağırılır

    for value in values:
        aldigi_puan, galibiyet, sb = o_ana_kadar_aldigi_puan(value, aldigi_puan, galibiyet, oyuncu_listesi, sb)
        kalan_tur = len(values) - values.index(value)
        sb, aldigi_puan = rakip_puanlari_al(value, rakipler_puan, oyuncu_listesi, aldigi_puan, kalan_tur, sb)

    return galibiyet, sb


# O ana kadar alınan puanı, galibiyet sayısını, sb puanına eklemeler yapılan fonk
def o_ana_kadar_aldigi_puan(value, aldigi_puan, galibiyet, oyuncu_listesi, sb):

    # BYE ve + geçilmeyen turlar için aldığı puan bir arttırılır
    # BYE ve + geçtiğinde aldığı 1 puan o turun hesaplaması bittikten sonra başka fonk eklenecektir
    if value[2] == 1 and value[0] != "-":  # Oyuncu bir puan almıştır. Tur BYE geçilmemiştir
        aldigi_puan += 1
        sb += sonneborn_berger(value[0], oyuncu_listesi)

    if (value[2] == 1 and value[0] != "-") or value[2] == "+":
        galibiyet += 1

    if value[2] == "½":  # 0.5 puan alınan durumda alınan puana ve sb puanına yapılacak eklemelerin yapıldığı koşul
        aldigi_puan += 0.5
        sb += sonneborn_berger(value[0], oyuncu_listesi) / 2

    return aldigi_puan, galibiyet, sb


# SB puanını eğer tur BYE ve + ile geçilmediyse rakip puanını listeden çekmeliyiz
# Bunun için oluşturulmuş fonk
def sonneborn_berger(value, oyuncu_listesi):
    for oyuncu in oyuncu_listesi:
        if oyuncu[0] == value:
            return oyuncu[5]


# Rakiplerin puanlarını listeye atayan
# Rakip gelmeme durumlarında ve bye geçme durumlarında listeye ve değişkenlere eklenecek verileri ekleyen fonk
def rakip_puanlari_al(value, rakipler_puan, oyuncu_listesi, aldigi_puan, kalan_tur, sb):

    # Oynanan oyun için rakip puanı alınır
    for oyuncu in oyuncu_listesi:
        if oyuncu[0] == value[0] and value[2] != "+" and value[2] != "-":
            rakipler_puan.append(oyuncu[5])

    # Rakip gelmeme durumları ve BYE geçme durumlarında kullanılacak olan koşul ifadesi
    if value[0] == "-" or value[2] == "+" or value[2] == "-":
        ek_puan = aldigi_puan + ((kalan_tur-1) * 0.5)  # Rakipler puanlarının tutulduğu listeye atanır
        rakipler_puan.append(ek_puan)

        # Bu işlemler o turda rakiplerin puanları atandıktan sonra yapılır
        # Daha önce yapılsaydı ek puan verisi yanlış hesaplanacaktı
        if value[2] == "+" or value[0] == "-":
            sb += ek_puan
            aldigi_puan += 1

    return sb, aldigi_puan


# Her turdan önce yapılacak olan eşleştirmelerin işlemlerinin başladığı fonk
def eslestirmeler(oyuncu_listesi, beyazlar, siyahlar, puanlar, oyuncu_dic):

    for oyuncu in oyuncu_listesi:
        bulundu = False  # Bulundu değeri True olduğunda artık o oyuncu için rakip aranmayacak

        # Eğer oyuncu eşleştiyse bir daha eşleşmeye katılmaması için puanlar listesinden çıkartılır
        if oyuncu not in beyazlar and oyuncu not in siyahlar and not bulundu:
            puanlar[oyuncu[5]].remove(oyuncu[0])

            # Puan keyleri sırasıyla çağrılır
            for value in puanlar.values():
                ayni_puana_sahip_bsno = value  # rakip olacabilecek kişi için bsno no alınır
                bulundu = asamalar(ayni_puana_sahip_bsno, oyuncu, beyazlar, siyahlar, oyuncu_dic, oyuncu_listesi)

                if bulundu:  # Rakip bulununca döngüden çıkar
                    break


# Belirtilen aşamaların uygulanacağı fonk
def asamalar(ayni_puana_sahip_bsno, oyuncu, beyazlar, siyahlar, oyuncu_dic, oyuncu_listesi):

    # 1.1
    for rakip in ayni_puana_sahip_bsno:

        # Oyuncu ve rakiple ilgili ihtiyacımız olacak olan veriler çağrılan fonk sayesinde elde edilir
        oyuncu1, oyuncu_renk, rakip1, rakip_renk = asama_verileri_al(oyuncu_dic, oyuncu, rakip)

        # Belli kurallar kontrol edilir
        if oyuncu_renk != rakip_renk and daha_once_eslestiler_mi(oyuncu_dic, oyuncu, rakip):

            if oyuncu_renk == "b" or rakip_renk == "s":
                rakip_beyaz_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)
            elif rakip_renk == "b" or oyuncu_renk == "s":
                rakip_siyah_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)

            return True

    # 1.2
    if oyuncu not in beyazlar or oyuncu not in siyahlar:

        # Oyuncu ve rakiple ilgili ihtiyacımız olacak olan veriler çağrılan fonk sayesinde elde edilir
        for rakip in ayni_puana_sahip_bsno:
            oyuncu1, oyuncu_renk, rakip1, rakip_renk = asama_verileri_al(oyuncu_dic, oyuncu, rakip)

            # Belli kurallar kontrol edilir
            if renk_kuralina_uygun_mu(oyuncu_dic, oyuncu_dic[rakip][-1][1], rakip) and daha_once_eslestiler_mi(oyuncu_dic, oyuncu, rakip):

                if oyuncu_renk == "b" or rakip_renk == "b":
                    rakip_beyaz_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)
                elif rakip_renk == "s" or oyuncu_renk == "s":
                    rakip_siyah_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)

                return True

    # 1.3
    if oyuncu not in beyazlar or oyuncu not in siyahlar:

        # Oyuncu ve rakiple ilgili ihtiyacımız olacak olan veriler çağrılan fonk sayesinde elde edilir
        for rakip in ayni_puana_sahip_bsno:
            oyuncu1, oyuncu_renk, rakip1, rakip_renk = asama_verileri_al(oyuncu_dic, oyuncu, rakip)

            # Belli kurallar kontrol edilir
            if renk_kuralina_uygun_mu(oyuncu_dic, oyuncu_dic[oyuncu[0]][-1][1], oyuncu[0]) and daha_once_eslestiler_mi(oyuncu_dic, oyuncu, rakip):

                if rakip_renk == "b" or oyuncu_renk == "b":
                    rakip_siyah_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)
                elif oyuncu_renk == "s" or rakip_renk == "s":
                    rakip_beyaz_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu)

                return True


# Oyuncu ve rakiple ilgili ihtiyacımız olacak olan verileri aldığımız fonk
def asama_verileri_al(oyuncu_dic, oyuncu, rakip):

    oyuncu1 = oyuncu_dic.get(oyuncu[0])
    oyuncu_renk = oyuncu1[-1][1]
    rakip1 = oyuncu_dic.get(rakip)
    rakip_renk = rakip1[-1][1]
    return oyuncu1, oyuncu_renk, rakip1, rakip_renk


# Beyazlar ve siyahlar listesine atama yapılır
def rakip_beyaz_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu):

    beyazlar.append(listeden_rakip_al(rakip, oyuncu_listesi))
    siyahlar.append(oyuncu)
    ayni_puana_sahip_bsno.remove(rakip)


# Beyazlar ve siyahlar listesine atama yapılır
def rakip_siyah_olacaksa(beyazlar, siyahlar, rakip, oyuncu_listesi, ayni_puana_sahip_bsno, oyuncu):

    beyazlar.append(oyuncu)
    siyahlar.append(listeden_rakip_al(rakip, oyuncu_listesi))
    ayni_puana_sahip_bsno.remove(rakip)


# Listeden rakiple ilgili tum bilgiler çekilir
# Beyazlar ve siyahlar listesi oluşturulurken oyuncular ilgili bütün bilgilerin listenin içinde liste şeklinde yer alması lazım
def listeden_rakip_al(rakip, oyuncu_listesi):
    for bsno in oyuncu_listesi:
        if bsno[0] == rakip:
            return bsno


# Renk kuralına uygunluk kontrol edilir
def renk_kuralina_uygun_mu(oyuncu_dic, renk, kisi):

    durum = True  # False olduğunda uygun olmadığı anlaşılır
    siyah, beyaz = 0, 0  # Daha önceden alınan siyah ve beyaz renk sayıları bu değişkenlerde tutulur.
    # Her eşleştirme yapılmadan önce ya oyuncu için ya da rakip için kontrol edilir
    value = oyuncu_dic.get(kisi)

    for i in value[::-1]:
        if i[1] == "b":
            beyaz += 1
        elif i[1] == "s":
            siyah += 1

        # Üst üste üç kez aynı rengi alamaz
        if beyaz == 2 and siyah == 0 and renk == "b":
            return False
        elif siyah == 2 and beyaz == 0 and renk == "s":
            return False

    #  Bir oyuncu bir rengi diğerinden en çok 2 kez fazla alabilir
    if renk == "s" and beyaz + 1 - siyah > 2:
        durum = False
    elif renk == "b" and siyah + 1 - beyaz > 2:
        durum = False

    return durum


# Daha önce eşleşip eşleşmedikleri bilgisini döndüren fonk
def daha_once_eslestiler_mi(oyuncu_dic, oyuncu, rakip):

    durum = True  # Eşleşmişler ise False değeri atanır
    values = oyuncu_dic.get(oyuncu[0])
    for value in values:
        if value[0] == rakip:
            durum = False
            return durum
    return durum


# Puanların keyleri oluşturduğu aynı puanı alanların aynı keyin value değerinde tutulacağı dic oluşturan fonk
def puanlar_listesi_olustur(puanlar, oyuncu_listesi):

    for oyuncu in oyuncu_listesi:
        puanlar.setdefault(oyuncu[5], []).append(oyuncu[0])


# Programın başında oyuncuların ve diğer verilerin alınacağı fonk
def verileri_al(oyuncu_listesi, tur_atla_durumu):

    oyuncu_verileri_al(oyuncu_listesi)
    ilk_siralama_islemi(oyuncu_listesi)
    listeye_bsno_ekle(oyuncu_listesi)
    dic_durum_ekleme(tur_atla_durumu, oyuncu_listesi)
    ilk_cikti(oyuncu_listesi)

    min_tur, max_tur = tur_sayisi_max_min(oyuncu_listesi)
    tur_sayisi = max_min_kontrol("Turnuvadaki tur sayisini giriniz ({},{}):", min_tur, max_tur)
    renk = renk_al()

    return tur_sayisi, renk


# Ad ve soyadları büyük harfe çevirir. Türkçe karakterlere uygun olarak
def buyuk_harfe_cevir(isim):

    turkce_karakter = [('i', 'İ'), ('ğ', 'Ğ'), ('ü', 'Ü'), ('ş', 'Ş'), ('ö', 'Ö'), ('ç', 'Ç'), ('ı', 'I')]

    for aranan, harf in turkce_karakter:
        isim = isim.replace(aranan, harf)
    isim = isim.upper()
    return isim


# Oyuncuların verilerini alır
def oyuncu_verileri_al(oyuncu_listesi):

    lisans_no = []  # Lisans no unique olup olmadığını kontrol ederken bu liste kullanılır
    # Her oyuncu lno alındıktan sonra bu listeye aktarılır

    lno = lno_kontrol(lisans_no)
    while lno > SIFIR:

        ad_soyad = input("Oyuncunun adini-soyadini giriniz: ")
        ad_soyad = buyuk_harfe_cevir(ad_soyad)
        elo = puan_kontrol(mesaj="Oyuncunun ELO’sunu giriniz (en az 1000, yoksa 0): ")
        ukd = puan_kontrol(mesaj="Oyuncunun UKD’sini giriniz (en az 1000, yoksa 0): ")

        # Oyuncu listesine oyuncunun bilgileri eklenir
        # Sıfırlar daha sonra puan ve eşitlik bozma puanları ile doldurulacaktır
        oyuncu_listesi.append([lno, ad_soyad, elo, ukd, 0, 0, 0, 0, 0])

        print("\n")
        lno = lno_kontrol(lisans_no)


# Lno kontrol edilir unique mi diye
# Eğer daha önce girilmiş bir lno ise while döngüsü doğru değer girilene kadar dönmeye devam eder
def lno_kontrol(lisans_no):

    veri = int(input("Oyuncunun lisans numarasini giriniz (bitirmek için 0 ya da negatif giriniz): "))
    while veri in lisans_no:
        veri = int(input("Oyuncunun lisans numarasini giriniz (bitirmek için 0 ya da negatif giriniz): "))

    lisans_no.append(veri)  # lno ların tutulduğu listeye bu lno da eklenir
    return veri


# Puanların doğru aralıklarda girilip girilmediğini kontrol eder ELO UKD
def puan_kontrol(mesaj):

    veri = int(input(mesaj))
    while not ((veri == SIFIR) or (veri >= BIN)):
        veri = int(input(mesaj))
    return veri


# Ad soyad türkçe alfabeye göre sıralanır
def ilk_siralama_islemi(oyuncu_listesi):
    alfabe = ' ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'
    oyuncu_listesi.sort(key=lambda oyuncu: (-oyuncu[2], -oyuncu[3], [alfabe.find(harf) for harf in oyuncu[1]], oyuncu[0]))


# Ad soyad türkçe alfabeye göre sıralanır
def siralama_islemi(oyuncu_listesi):
    alfabe = ' ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'
    oyuncu_listesi.sort(key=lambda oyuncu: (-oyuncu[5], -oyuncu[3], -oyuncu[4], [alfabe.find(harf) for harf in oyuncu[2]], oyuncu[1]))


# İlk sıralama yapıldıktan sonra oyuncu listesine oyuncuların ilk indexlerine bsno ları aktarılır
def listeye_bsno_ekle(oyuncu_listesi):
    bsno = 1
    for oyuncu in oyuncu_listesi:
        oyuncu.insert(0, bsno)
        bsno += 1


# Tur atlayan ya da rakibi gelmeyen oyuncuların bilgilerinin tutulacağı dic oluşturan fonk
def dic_durum_ekleme(tur_atla_durumu, oyuncu_listesi):
    for oyuncu in oyuncu_listesi:
        tur_atla_durumu.insert(oyuncu[0], False)


# Max ve min girilebilecek tur sayısını alan fonk
def tur_sayisi_max_min(oyuncular_liste):
    oyuncu_sayisi = len(oyuncular_liste)
    min_tur = math.log(oyuncu_sayisi, 2)
    max_tur = oyuncu_sayisi-1
    return math.ceil(min_tur), max_tur


# Elo ve Ukd puanlarını kontrol eder
# Kullanıcıya gösterilecek mesaj ve max min sayı lar parametrelere atanır
def max_min_kontrol(mesaj, min_sayi, max_sayi):

    veri = int(input(mesaj.format(min_sayi, max_sayi)))
    while veri < min_sayi or veri > max_sayi:
        veri = int(input(mesaj.format(min_sayi, max_sayi)))
    return veri


# Renk verisini kontrol eder
def renk_al():

    renk = input("Baslangic siralamasina gore ilk oyuncunun ilk turdaki rengini giriniz (b/s): ")
    while renk not in ["b", "s"]:
        renk = input("Baslangic siralamasina gore ilk oyuncunun ilk turdaki rengini giriniz (b/s): ")
    return renk


# İlk sıralama çıktısını yazar
def ilk_cikti(oyuncular_listesi):

    print("\nBaşlangıç Sıralama Listesi:")
    print("BSNo   LNo Ad-Soyad      ELO  UKD")
    print("---- ----- ------------ ---- ----")
    for oyuncu in oyuncular_listesi:
        print(format(oyuncu[0], "4"), format(oyuncu[1], "5"), oyuncu[2], " " * (12 - len(oyuncu[2])), end="")
        print(format(oyuncu[3], "4"), format(oyuncu[4], "4"))


# Listede tek kalan olup olmayacağını bu fonk sayesinde bir değişkene atarız
# Değişken koşul ifadelerinde kullanılır
def liste_tek_mi_cift_mi(oyuncu_listesi):

    tek_kalan_durum = False  # Tek kalan oyuncu olacaksa True değerini alır
    if len(oyuncu_listesi) % 2 == 1:
        tek_kalan_durum = True
    return tek_kalan_durum


# İlk turun eşleştirmelerini yapacak, tur çıktısını yazdıracak ve puanları alacak fonk içerir
def ilk_tur(oyuncu_listesi, tur_atla_durum, tek_kalan_durum, oyuncu_dic, masa_sayisi, renk):

    beyazlar = []  # Beyazlarla oynayacak oyuncular bu listeye eklenir ve iki boyutlu liste oluşur
    siyahlar = []  # Siyahlarla oynayacak oyuncular bu listeye eklenir ve iki boyutlu liste oluşur
    tek_kalan = []  # Tek kalan kişinin bilgileri eklenir

    # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
    if tek_kalan_durum:
         tek_kalan = tek_kalan_al(tur_atla_durum, oyuncu_listesi, tek_kalan)

    ilk_tur_beyaz_siyah(oyuncu_listesi, siyahlar, beyazlar, oyuncu_dic, renk)

    # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
    if tek_kalan_durum:
        oyuncu_dic.setdefault(tek_kalan[0][0], [])

    tur_ciktilari(-1, siyahlar, beyazlar, tek_kalan)
    puan_al(oyuncu_listesi, oyuncu_dic, beyazlar, siyahlar, masa_sayisi, tek_kalan, tur_atla_durum, tek_kalan_durum)

    # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
    if tek_kalan_durum:
        oyuncu_listesi.append(tek_kalan[0])


# İlk tur beyazlar ve siyahların olacağı iki boyutlu listeler girilen renk ve oyuncunun indexine göre belirlenir
# Aynı anda oyuncu dic keyler oyuncuların bsno olacak valueları da liste olacak şekilde oluşturulur
def ilk_tur_beyaz_siyah(oyuncu_listesi, siyahlar, beyazlar, oyuncu_dic, renk):

    for oyuncu in oyuncu_listesi:

        if renk == "s":  # Renk olarak siyah girildiyse
            if oyuncu_listesi.index(oyuncu) % 2 == 0:
                siyahlar.append(oyuncu)
                oyuncu_dic.setdefault(oyuncu[0], [])
            else:
                beyazlar.append(oyuncu)
                oyuncu_dic.setdefault(oyuncu[0], [])
        else:  # Renk olarak beyaz girildiyse
            if oyuncu_listesi.index(oyuncu) % 2 == 0:
                beyazlar.append(oyuncu)
                oyuncu_dic.setdefault(oyuncu[0], [])
            else:
                siyahlar.append(oyuncu)
                oyuncu_dic.setdefault(oyuncu[0], [])


# Tur eşleşmeleri yapıldıktan sonra her tur için bu çıktı yazdırılır
def tur_ciktilari(tur_sayisi, siyahlar, beyazlar, tek_kalan):

    print("\n\n{}. Tur Eşleştirme Listesi:".format(tur_sayisi+2))
    print("       Beyazlar        Siyahlar")
    print("MNo BSNo LNo Puan  -  Puan LNo BSNo")
    print("--- ---- --- ----  -  ---- --- ----")

    for oyuncu in range(len(beyazlar)):
        print(format(oyuncu+1, "3"), end=" ")
        print(format(beyazlar[oyuncu][0], "4"), format(beyazlar[oyuncu][1], "3"), format(beyazlar[oyuncu][5], ".2f"), end="  -  ")
        print(format(siyahlar[oyuncu][5], ".2f"), format(siyahlar[oyuncu][1], "3"), format(siyahlar[oyuncu][0], "4"))
    if len(tek_kalan) != 0:
        print(format(len(beyazlar)+1, "3"), format(tek_kalan[0][0], "4"), format(tek_kalan[0][1], "3"), end=" ")
        print(format(tek_kalan[0][5], ".2f"), " - ", "BYE")
    print("\n")


# Her tur için tek kalan kişi belirleyen fonk
def tek_kalan_al(tur_atla_durum, oyuncu_listesi, tek_kalan):

    for oyuncu in oyuncu_listesi[::-1]:  # Listenin sonundan başlar çünkü sonda en düşük puana sahip oyuncu vardır
        if not tur_atla_durum[oyuncu[0]-1]:  # Tur atladıysa ya da rakip gelmediyse bir daha tur atlayamaz
            tek_kalan.append(oyuncu)
            oyuncu_listesi.remove(oyuncu)
            tur_atla_durum[oyuncu[0]-1] = True  # Tur atladığı bilgisi tek_atla_durum dic de güncellenmelidir
            return tek_kalan


# Her tur sonunda masalara verilen puanlara göre oyunculara puanlar atanır
# Bu işlemleri gerçekleştiren fonk
def puan_al(oyuncu_listesi, oyuncu_dic, beyazlar, siyahlar, masa_sayisi, tek_kalan, tur_atla_durum, tek_kalan_durum):

    for sayac in range(masa_sayisi):
        s_bsno = siyahlar[sayac][0]  # Siyahta oynayan oyuncunun bsno
        b_bsno = beyazlar[sayac][0]  # Beyazda oynayan oyuncunun bsno
        # Masa için girilen değer
        sayi = max_min_kontrol("1. turda 1. masada oynanan macin sonucunu giriniz (0-5): ".format(sayac), 0, 5)
        # Bu sayının oyuncular için hangi puanlara denk geldiğini belirleyecek fonk çağrılır
        s_puan, b_puan = hangi_puan(sayi, tur_atla_durum, s_bsno, b_bsno)
        # Oyuncu dic tur verileri aktarılmalıdır
        oyuncu_dic[s_bsno].append([b_bsno, "s", s_puan])
        oyuncu_dic[b_bsno].append([s_bsno, "b", b_puan])
        # Oyuncu listesine o oyuncun puanı eklenmelidir
        listeye_puan_ekleme(s_puan, oyuncu_listesi, s_bsno)
        listeye_puan_ekleme(b_puan, oyuncu_listesi, b_bsno)

    # Tek kalan olmacaksa programın birden sonlanmaması için bu koşul ifadesi kullanılır.
    if tek_kalan_durum:
        oyuncu_dic[tek_kalan[0][0]].append(["-", "-", 1])  # dic oyuncunun tur bilgisi olmalıdır
        tek_kalan[0][5] += 1  # listede oyuncunun puan bilgisi güncellenmelidir


# Listeye oyuncunun o turda aldığı puanı eklenir
def listeye_puan_ekleme(puan, oyuncu_listesi, bsno):

    for liste in oyuncu_listesi:
        if liste[0] == bsno and puan not in ["½", "+", "-"]:
            liste[5] += puan
        elif liste[0] == bsno and puan == "½":
            liste[5] += PUAN_SIFIR_NOKTA_BES
        elif liste[0] == bsno and puan == "+":
            liste[5] += PUAN_BIR


# Masa için girilen sayının oyuncular için hangi puanı ifade ettiğini verecek olan fonk
# Aynı zamanda oyun oynamadığı için tur atlama durumunun değişmesi gereken oyuncuların bilgileri güncellenir
def hangi_puan(sayi, tur_atla_durum, s_bsno, b_bsno):

    if sayi == PUAN_SIFIR:
        s_puan = "½"
        b_puan = "½"
    elif sayi == MAC_SONUCU_BIR:
        s_puan = PUAN_SIFIR
        b_puan = PUAN_BIR
    elif sayi == MAC_SONUCU_IKI:
        s_puan = PUAN_BIR
        b_puan = PUAN_SIFIR
    elif sayi == MAC_SONUCU_UC:
        s_puan = "-"
        b_puan = "+"
        tur_atla_durum[b_bsno - 1] = True
    elif sayi == MAC_SONUCU_DORT:
        s_puan = "+"
        b_puan = "-"
        tur_atla_durum[s_bsno - 1] = True
    else:
        s_puan = "-"
        b_puan = "-"

    return s_puan, b_puan


main()
