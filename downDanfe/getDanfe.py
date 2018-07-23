from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import deathbycaptcha
import base64

client = deathbycaptcha.SocketClient('operating', 'Operating1')

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "pdfs","plugins.always_open_pdf_externally": True, "download.prompt_for_download": False,}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

def getDanfe(chave):
    driver.get('https://www.webdanfe.com.br/danfe/index.html')
    campo_chave = driver.find_element_by_xpath('//*[@id="chaveNfe"]')
    campo_chave = campo_chave.send_keys(chave)
    driver.find_element_by_xpath('//*[@id="one"]/table/tbody/tr[4]/td/center/input[1]').click()
    
    imgCaptcha = driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_LabelCaptcha"]/img')
    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, imgCaptcha)
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    captchaText = client.decode('captcha.jpg',60)
    captchaField = driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_LabelCaptchaInput"]')
    captchaField = captchaField.send_keys(captchaText['text'])

    driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_ButtonGerarDanfe"]').click()
    try:
        driver.find_element_by_xpath('/html/body/span/h1/text()')
        driver.find_element_by_xpath('/html/body/span/h2/i')
    except:
        ('runnin')

danfelist = ['29160407069951000166550010000000591900001307',
'29160407069951000166550010000000601910770029',
'29160407069951000166550010000000621090091032',
'29160407069951000166550010000000631160080023',
'29160407069951000166550010000000641680097203',
'29160407069951000166550010000000651204002051',
'29160407069951000166550010000000661010055009',
'29160407069951000166550010000000671045800050',
'29160407069951000166550010000000681202060374',
'29160407069951000166550010000000691687000899',
'29160407069951000166550010000000701810408600',
'29160407069951000166550010000000711000055006',
'29160407069951000166550010000000721770000375',
'29160407069951000166550010000000731310080259',
'29160407069951000166550010000000741090093206',
'29160407069951000166550010000000751000070071',
'29160407069951000166550010000000761082106056',
'29160407069951000166550010000000771500024057',
'29160407069951000166550010000000781290502001',
'29160407069951000166550010000000791882020905',
'29160407069951000166550010000000801950026005',
'29160407069951000166550010000000811000004009',
'29160407069951000166550010000000821732302145',
'29160407069951000166550010000000831463430023',
'29160407069951000166550010000000841040032609',
'29160407069951000166550010000000851003533010',
'29160407069951000166550010000000861024604401',
'29160407069951000166550010000000871250206206',
'29160407069951000166550010000000881479805400',
'29160407069951000166550010000000891770400915',
'29160407069951000166550010000000901580800000',
'29160407069951000166550010000000921000700157',
'29160407069951000166550010000000911005231409',
'29160407069951000166550010000000931900901008',
'29160407069951000166550010000000941088015352',
'29160407069951000166550010000000951000000009',
'29160507069951000166550010000000961095008941',
'29160507069951000166550010000000971060000100',
'29160507069951000166550010000000981000363506',
'29160507069951000166550010000000991001000030',
'29160507069951000166550010000001001014000818',
'29160507069951000166550010000001011600802907',
'29160507069951000166550010000001031042948059',
'29160507069951000166550010000001041100001990',
'29160507069951000166550010000001051005200105',
'29160507069951000166550010000001081080818023',
'29160507069951000166550010000001061095008311',
'29160507069951000166550010000001071080402040',
'29160507069951000166550010000001091602840200',
'29160507069951000166550010000001101589000543',
'29160507069951000166550010000001111390001802',
'29160507069951000166550010000001131600802908',
'29160507069951000166550010000001121008208063',
'29160507069951000166550010000001141000700052',
'29160507069951000166550010000001021300000004',
'29160507069951000166550010000001151400101358',
'29160507069951000166550010000001161100020708',
'29160507069951000166550010000001171000000907',
'29160507069951000166550010000001181800382283',
'29160507069951000166550010000001191300000605',
'29160507069951000166550010000001201000008008',
'29160507069951000166550010000001211901807005',
'29160507069951000166550010000001221000006204',
'29160507069951000166550010000001231435252044',
'29160507069951000166550010000001241403006045',
'29160507069951000166550010000001251810004405',
'29160507069951000166550010000001261920200001',
'29160507069951000166550010000001271001104036',
'29160507069951000166550010000001291073701590',
'29160507069951000166550010000001281030060162',
'29160507069951000166550010000001301040000004',
'29160607069951000166550010000001311231109060',
'29160607069951000166550010000001321045030902',
'29160607069951000166550010000001331603002119',
'29160607069951000166550010000001341001080003',
'29160607069951000166550010000001351085402926',
'29160607069951000166550010000001361800300807',
'29160607069951000166550010000001371066500939',
'29160607069951000166550010000001381200043433',
'29160607069951000166550010000001391003403043',
'29160607069951000166550010000001401080159047',
'29160607069951000166550010000001431405730009',
'29160607069951000166550010000001411800751469',
'29160607069951000166550010000001441080005065',
'29160607069951000166550010000001451059086806',
'29160607069951000166550010000001461078708105',
'29160607069951000166550010000001481403022500',
'29160607069951000166550010000001491080000000',
'29160607069951000166550010000001501500753201',
'29160607069951000166550010000001471000070380',
'29160607069951000166550010000001511950102152',
'29160607069951000166550010000001521800406005',
'29160607069951000166550010000001541000555809',
'29160607069951000166550010000001561666851304',
'29160607069951000166550010000001571400100703',
'29160607069951000166550010000001581000050072',
'29160607069951000166550010000001591085108000',
'29160607069951000166550010000001551270707056',
'29160607069951000166550010000001601007030946',
'29160607069951000166550010000001611211002103',
'29160607069951000166550010000001621067790739',
'29160607069951000166550010000001631679000515',
'29160607069951000166550010000001641479100017',
'29160607069951000166550010000001651770002805',
'29160607069951000166550010000001661080902005',
'29160607069951000166550010000001671586406952',
'29160607069951000166550010000001691000674312',
'29160607069951000166550010000001681760061002',
'29160707069951000166550010000001731500090863',
'29160707069951000166550010000001701001870080',
'29160707069951000166550010000001711030000001',
'29160707069951000166550010000001741410502078',
'29160707069951000166550010000001721004090004',
'29160707069951000166550010000001751209000130',
'29160707069951000166550010000001771032063098',
'29160707069951000166550010000001781050603004',
'29160707069951000166550010000001761000004803',
'29160707069951000166550010000001791003059201',
'29160707069951000166550010000001801030300039',
'29160707069951000166550010000001811073319006',
'29160707069951000166550010000001821104040803',
'29160707069951000166550010000001831003246071',
'29160707069951000166550010000001841490200029',
'29160707069951000166550010000001851553590519',
'29160707069951000166550010000001861006600757',
'29160707069951000166550010000001881408809000',
'29160707069951000166550010000001891000060051',
'29160707069951000166550010000001911018650916',
'29160707069951000166550010000001921766020021',
'29160707069951000166550010000001901060020995',
'29160707069951000166550010000001951064000979',
'29160707069951000166550010000001961010909070',
'29160707069951000166550010000001971250000899',
'29160707069951000166550010000002011504940000',
'29160707069951000166550010000001981590031020',
'29160707069951000166550010000001941045060409',
'29160707069951000166550010000002021099700620',
'29160707069951000166550010000001991201000605',
'29160707069951000166550010000002001763005106',
'29160707069951000166550010000002031070002302',
'29160707069951000166550010000002041020901572',
'29160707069951000166550010000002051200500603',
'29160707069951000166550010000002061001500201',
'29160707069951000166550010000002071040020506',
'29160807069951000166550010000002081807111609',
'29160807069951000166550010000002151805000430',
'29160807069951000166550010000002131983024276',
'29160807069951000166550010000002161009700005',
'29160807069951000166550010000002141000006721',
'29160807069951000166550010000002121200200039',
'29160807069951000166550010000002101003400073',
'29160807069951000166550010000002171000002000',
'29160807069951000166550010000002201000300074',
'29160807069951000166550010000002211007080905',
'29160807069951000166550010000002221308500005',
'29160807069951000166550010000002231009001004',
'29160807069951000166550010000002241070180107',
'29160807069951000166550010000002251000715084',
'29160807069951000166550010000002261730400600',
'29160807069951000166550010000002271277030394',
'29160807069951000166550010000002281606000187',
'29160807069951000166550010000002291229303097',
'29160807069951000166550010000002301060500009',
'29160807069951000166550010000002311300017002',
'29160807069951000166550010000002321000200364',
'29160807069951000166550010000002331525560654',
'29160807069951000166550010000002341635098405',
'29160807069951000166550010000002351607675000',
'29160807069951000166550010000002361005000001',
'29160807069951000166550010000002371596618000',
'29160807069951000166550010000002381086000257',
'29160807069951000166550010000002391601010200',
'29160807069951000166550010000002401009047609',
'29160807069951000166550010000002411909563007',
'29160807069951000166550010000002421090049039',
'29160807069951000166550010000002431083010006',
'29160807069951000166550010000002441805080001',
'29160807069951000166550010000002451060800013',
'29160807069951000166550010000002461080235734',
'29160807069951000166550010000002471006346096',
'29160807069951000166550010000002481030000908',
'29160807069951000166550010000002491480300373',
'29160807069951000166550010000002501040589007',
'29160807069951000166550010000002511602000075',
'29160807069951000166550010000002521320203014',
'29160807069951000166550010000002531077454395',
'29160807069951000166550010000002541012056503',
'29160807069951000166550010000002551708801003',
'29160807069951000166550010000002561610002819',
'29160807069951000166550010000002571200030003',
'29160807069951000166550010000002581009438050',
'29160807069951000166550010000002591000410206',
'29160807069951000166550010000002601000620007',
'29160807069951000166550010000002611066060007',
'29160807069951000166550010000002621010001622',
'29160807069951000166550010000002631003083004',
'29160807069951000166550010000002641007019022',
'29160807069951000166550010000002651050007003',
'29160807069951000166550010000002661001006888',
'29160907069951000166550010000002671104007004',
'29160907069951000166550010000002681650860217',
'29160907069951000166550010000002691300021841',
'29160907069951000166550010000002701021905906',
'29160907069951000166550010000002711153650201',
'29160907069951000166550010000002721276080052',
'29160907069951000166550010000002731002320916',
'29160907069951000166550010000002741837042000',
'29160907069951000166550010000002751001002087',
'29160907069951000166550010000002761000057039',
'29160907069951000166550010000002771100050343',
'29160907069951000166550010000002781600190001',
'29160907069951000166550010000002791173050275',
'29160907069951000166550010000002801400000045',
'29160907069951000166550010000002811726000118',
'29160907069951000166550010000002821007035720',
'29160907069951000166550010000002831030800834',
'29160907069951000166550010000002841000047000',
'29160907069951000166550010000002851700002180',
'29160907069951000166550010000002861478008242',
'29160907069951000166550010000002871890200306',
'29160907069951000166550010000002881079010400',
'29160907069951000166550010000002891501001700',
'29160907069951000166550010000002901003057004',
'29160907069951000166550010000002911001002730',
'29160907069951000166550010000002961000060008',
'29160907069951000166550010000002971000003044',
'29160907069951000166550010000002981032580001',
'29160907069951000166550010000002921490060884',
'29160907069951000166550010000002991017360702',
'29160907069951000166550010000003001400875003',
'29160907069951000166550010000003011304201061',
'29160907069951000166550010000003021000054007',
'29160907069951000166550010000003031200002008',
'29160907069951000166550010000003041500040905',
'29160907069951000166550010000003051009000408',
'29160907069951000166550010000003061100009045',
'29160907069951000166550010000003071000920070',
'29160907069951000166550010000003081049090000',
'29160907069951000166550010000003091069600800',
'29160907069951000166550010000003101070900006',
'29160907069951000166550010000003111347067800',
'29160907069951000166550010000003121032400004',
'29160907069951000166550010000003131030005059',
'29160907069951000166550010000003141008302108',
'29160907069951000166550010000003151370902809',
'29160907069951000166550010000003161004023098',
'29160907069951000166550010000003171003619067',
'29160907069951000166550010000003181000620100',
'29160907069951000166550010000003191900800004',
'29160907069951000166550010000003201131720491',
'29160907069951000166550010000003211890130000',
'29160907069951000166550010000003221660000004',
'29160907069951000166550010000003231005090044',
'29160907069951000166550010000003241000000850',
'29160907069951000166550010000003251000053099',
'29160907069951000166550010000003261055414031',
'29160907069951000166550010000003271003400070',
'29160907069951000166550010000003281020020805',
'29160907069951000166550010000003401605205072',
'29160907069951000166550010000003411010000005',
'29160907069951000166550010000003421000020000',
'29161007069951000166550010000003431020460542',
'29161007069951000166550010000003441200050005',
'29161007069951000166550010000003451335550003',
'29161007069951000166550010000003461001000029',
'29161007069951000166550010000003471066202693',
'29161007069951000166550010000003481780304813',
'29161007069951000166550010000003491706047567',
'29161007069951000166550010000003501703175808',
'29161007069951000166550010000003511080798088',
'29161007069951000166550010000003521506550970',
'29161007069951000166550010000003531803915457',
'29161007069951000166550010000003541000508004',
'29161007069951000166550010000003551000010933',
'29161007069951000166550010000003561000010663',
'29161007069951000166550010000003571002324034',
'29161007069951000166550010000003581011806507',
'29161007069951000166550010000003591092370701',
'29161007069951000166550010000003601690080201',
'29161007069951000166550010000003611072005003',
'29161007069951000166550010000003621030510904',
'29161007069951000166550010000003631980300800',
'29161007069951000166550010000003641400004042',
'29161007069951000166550010000003651000069071',
'29161007069951000166550010000003661010002066',
'29161007069951000166550010000003671700790096',
'29161007069951000166550010000003681000827008',
'29161007069951000166550010000003691280006007',
'29161007069951000166550010000003701302000910',
'29161007069951000166550010000003711630010006',
'29161007069951000166550010000003721000210003',
'29161007069951000166550010000003731800001007',
'29161007069951000166550010000003741002002690',
'29161007069951000166550010000003751400600005',
'29161007069951000166550010000003761404051003',
'29161007069951000166550010000003771008340409',
'29161007069951000166550010000003781008300005',
'29161007069951000166550010000003791240300008',
'29161007069951000166550010000003801389902470',
'29161007069951000166550010000003811080600058',
'29161007069951000166550010000003821499509719',
'29161007069951000166550010000003831081152002',
'29161007069951000166550010000003841096007000',
'29161007069951000166550010000003851000065508',
'29161007069951000166550010000003861320590201',
'29161007069951000166550010000003871042030294',
'29161007069951000166550010000003881316000904',
'29161007069951000166550010000003891020600009',
'29161107069951000166550010000003901505230003',
'29161107069951000166550010000003911000000571',
'29161107069951000166550010000003921300070068',
'29161107069951000166550010000003931300170353',
'29161107069951000166550010000003941307090000',
'29161107069951000166550010000003951967440706',
'29161107069951000166550010000003961040130650',
'29161107069951000166550010000003971050009002',
'29161107069951000166550010000003981150757393',
'29161107069951000166550010000003991000492006',
'29161107069951000166550010000004001600000034',
'29161107069951000166550010000004011501080703',
'29161107069951000166550010000004021070200001',
'29161107069951000166550010000004031800082001',
'29161107069951000166550010000004041008748001',
'29161107069951000166550010000004051407120003',
'29161107069951000166550010000004061400800057',
'29161107069951000166550010000004071560300076',
'29161107069951000166550010000004081014202340',
'29161107069951000166550010000004091429295042',
'29161107069951000166550010000004101741109047',
'29161107069951000166550010000004111002000514',
'29161107069951000166550010000004131506530082',
'29161107069951000166550010000004141140005017',
'29161107069951000166550010000004151000075788',
'29161107069951000166550010000004161060005007',
'29161107069951000166550010000004121975989609',
'29161107069951000166550010000004171000083009',
'29161107069951000166550010000004181030944000',
'29161107069951000166550010000004191300933070',
'29161107069951000166550010000004201309000042',
'29161107069951000166550010000004211092720003',
'29161107069951000166550010000004221109958000',
'29161107069951000166550010000004231250776475',
'29161107069951000166550010000004241300950004',
'29161107069951000166550010000004251061020009',
'29161107069951000166550010000004261003000006',
'29161107069951000166550010000004271104442907',
'29161107069951000166550010000004281503570310',
'29161107069951000166550010000004291812101070',
'29161107069951000166550010000004301333000614',
'29161107069951000166550010000004311050700205',
'29161207069951000166550010000004321000006403',
'29161207069951000166550010000004331200508051',
'29161207069951000166550010000004341001789023',
'29161207069951000166550010000004351060904604',
'29161207069951000166550010000004361010070049',
'29161207069951000166550010000004371552009549',
'29161207069951000166550010000004381037300007',
'29161207069951000166550010000004391434756004',
'29161207069951000166550010000004401708099006',
'29161207069951000166550010000004411309938001',
'29161207069951000166550010000004421590300034',
'29161207069951000166550010000004431000280800',
'29161207069951000166550010000004441070076002',
'29161207069951000166550010000004451200950049',
'29161207069951000166550010000004461000500900',
'29161207069951000166550010000004471047060504',
'29161207069951000166550010000004481008009673',
'29161207069951000166550010000004491083900007',
'29161207069951000166550010000004501301701028',
'29161207069951000166550010000004511902088093',
'29161207069951000166550010000004521010000702',
'29161207069951000166550010000004531407039002',
'29161207069951000166550010000004541620010021',
'29161207069951000166550010000004551010900063',
'29161207069951000166550010000004571039043473',
'29161207069951000166550010000004581062500670',
'29161207069951000166550010000004591100024857',
'29161207069951000166550010000004601169203506',
'29161207069951000166550010000004611773900001',
'29161207069951000166550010000004621102000004',
'29161207069951000166550010000004631300153025',
'29161207069951000166550010000004641089001612',
'29161207069951000166550010000004651040008122',
'29161207069951000166550010000004661055160003',
'29161207069951000166550010000004671020102810',
'29161207069951000166550010000004681870217001',
'29170107069951000166550010000004691000006000',
'29170107069951000166550010000004701947260031',
'29170107069951000166550010000004711000519706',
'29170107069951000166550010000004721020039952',
'29170107069951000166550010000004731200653370',
'29170107069951000166550010000004741009030604',
'29170107069951000166550010000004751306372000',
'29170107069951000166550010000004761130000006',
'29170107069951000166550010000004771008020003',
'29170107069951000166550010000004781100040403',
'29170107069951000166550010000004791501146005',
'29170107069951000166550010000004801600005044',
'29170107069951000166550010000004811000200781',
'29170107069951000166550010000004821004081881',
'29170107069951000166550010000004831070020604',
'29170107069951000166550010000004841000050005',
'29170107069951000166550010000004851350090062',
'29170107069951000166550010000004861901097782',
'29170107069951000166550010000004871000000603',
'29170107069951000166550010000004881800007707',
'29170107069951000166550010000004891005540309',
'29170107069951000166550010000004901071800101',
'29170107069951000166550010000004911900031559',
'29170107069951000166550010000004921300100000',
'29170107069951000166550010000004931564018003',
'29170107069951000166550010000004941550030097',
'29170107069951000166550010000004951200359003',
'29170107069951000166550010000004961440800020',
'29170107069951000166550010000004971050045003',
'29170107069951000166550010000004981806507082',
'29170107069951000166550010000004991600080030',
'29170107069951000166550010000005001410007490',
'29170107069951000166550010000005011003000001',
'29170107069951000166550010000005021990294002',
'29170107069951000166550010000005031000000080',
'29170107069951000166550010000005041400062862',
'29170107069951000166550010000005051006000001',
'29170107069951000166550010000005061080000904',
'29170107069951000166550010000005071070600116',
'29170107069951000166550010000005081708006125',
'29170107069951000166550010000005091905029001',
'29170107069951000166550010000005101000014078',
'29170107069951000166550010000005111600053101',
'29170207069951000166550010000005121000182106',
'29170207069951000166550010000005131767004293',
'29170207069951000166550010000005141000259006',
'29170207069951000166550010000005151903408006',
'29170207069951000166550010000005171044000034',
'29170207069951000166550010000005181800100027',
'29170207069951000166550010000005191900097696',
'29170207069951000166550010000005201800800094',
'29170207069951000166550010000005211995002556',
'29170207069951000166550010000005221156080994',
'29170207069951000166550010000005231164904078',
'29170207069951000166550010000005241049509002',
'29170207069951000166550010000005251053730076',
'29170207069951000166550010000005261693570060',
'29170207069951000166550010000005271007006047',
'29170207069951000166550010000005281070800038',
'29170207069951000166550010000005291039502001',
'29170207069951000166550010000005301940308300',
'29170207069951000166550010000005311008105904',
'29170207069951000166550010000005321000000086',
'29170207069951000166550010000005331407719005',
'29170207069951000166550010000005341317100356',
'29170207069951000166550010000005351204000000',
'29170207069951000166550010000005361620029063',
'29170207069951000166550010000005371004100200',
'29170207069951000166550010000005381035000094',
'29170207069951000166550010000005391056001046',
'29170207069951000166550010000005401700110021',
'29170207069951000166550010000005411107903805',
'29170207069951000166550010000005421363509263',
'29170207069951000166550010000005431244760202',
'29170207069951000166550010000005441300004002',
'29170207069951000166550010000005451260100640',
'29170207069951000166550010000005461460305072',
'29170207069951000166550010000005471259807497']

for item in danfelist:
    try:
        getDanfe(item)
    except:
        print("erro "+item)
        getDanfe(item)