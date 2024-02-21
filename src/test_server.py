import requests
import time

url = "https://api-datos-sunat.pacasoft.cloud/api/v1/ruc/"
values = ['10181126235', '10060187156', '10750752115', '10182128517', '10304122485', '10750111055', '10214770348', '15219219633', '20600192711', '10423470131', '10087721430', '10027912341', '10435677911', '10028493385', '10075397564', '10455585291', '10478541738', '10233714394', '10464755441', '10732979137', '10467840539', '10757951831', '10180412021', '15607401346', '10018691880', '10092844116', '10092548576', '10805946143', '10295525199', '10407057371', '10705460413', '10701009857', '10227024319', '10748119341', '20607909696', '10721575344', '10704989801', '10727145872', '10726456530', '10035855098', '10247863643', '20514411507', '10444656820', '10802327710', '20601275521', '15603801897', '10466678207', '10329336129', '10227308724', '10413440136', '10100440259', '10459796377', '10214324577', '10292321533', '10401413087', '20611661488', '20610799389', '10474920068', '10463039823', '10068329863', '10328115994', '10098786924', '10266207684', '10409981297', '10106067550', '10062339743', '10107343950', '10729183844', '20603100744', '20295677512', '10075367746', '20605645578', '10031012762', '20600242637', '17193022537', '10328687165', '10073032810', '10801525895', '10483662489', '10420162010', '10065449647', '10074258676', '10455386778', '10002175831', '10181999921', '10612669231', '10180959802', '10255227675', '10087868988', '20601416230', '10429132563', '10441164489', '10764220281', '10001124094', '10461648636', '10107024731', '10024423064', '10095151774', '10436801551', '10104415321', '10069821559', '10424451717', '20604455023', '10165948063', '15508437428', '10749711723', '10159605448', '10704285766', '10164649810', '20453383637', '10765865277', '10206802419', '10080184722', '10441719464', '10758919175', '10780181775', '10066071541', '10167837013', '10084131119', '10403517513', '10707352138', '20534204354', '10168078973', '10703294460', '10706772419', '10057123597', '10180989680', '10159596325', '10078776299', '10433113468', '10727955556', '10266885526', '10472644292', '10107771633', '20556865991', '10710776852', '10747564715', '10255825491', '10036867057', '10726176341', '10469399511', '20102026803', '10078817424', '10435920603', '10276731969', '10053958341', '10307720782', '20543420710', '10774272009', '10762330275', '10296983905', '10239061422', '10768105346', '20519960975', '20529946911', '10742153679', '10285998196', '10705369378', '10722529630', '10456985322', '10309609269', '10703964350', '10083144764', '10426533664', '10738745103', '10406836016', '10103975773', '20482693467', '10009296820', '10078998500', '20521893495', '10434889702', '20487395715', '10738897990', '10442101626', '15611518363', '10089153081', '10462891330', '10736688692', '10407765651', '10724023041', '10716156121', '10214492852', '10046404942', '10232632360', '10091597620', '10710183096', '10453750022', '10071646900', '10232543618', '10448191678', '10294702992', '10748420628', '10085536554', '10314735531', '10428199982', '10704767159', '10763899336', '10332470715', '10761499845', '10458487273', '10783660615', '10453809795', '10755822642', '10435293676', '10181702881', '10490204089', '10068669044', '10293028678', '20538998207', '10735749264', '10460788795', '10479061683', '10482714175', '10239336936', '10066144025', '20109012786', '20605570403', '20604591831', '10428464848', '10423653715', '20600725981', '20609438909', '10762476474', '10000385978', '10404335052', '10106533216', '10428104167', '10707514979', '20604849226', '10454517526', '10708096372', '20278884610', '10425850828', '10208973229', '10085928975', '10334331437', '10071939966', '10067741965', '10742436867', '10077458218', '10416556518', '10451971188', '10805636187', '20101757634', '10009064503', '10154084474', '10104051061', '10328683241', '10467743703', '10333374451', '10456732734', '10728424350', '10091556656', '10402408338', '10408842625', '10734862440', '10444100252', '10709699747', '10707644490', '20530890628', '10412166065', '10025563757', '10411453338', '10028391591', '10441805441', '10052214128', '10328521291', '15609024990', '10462619851', '10081898699', '20607618144', '10703584026', '10800453785', '10021454660', '10449308781', '10008231040', '10100727876', '10409666677', '10038543445', '10079967438', '10485838053', '10733640664', '15606165142', '10455820575', '10455965247', '20486970970', '10296987609', '10401846366', '15557794571', '15608216267', '10078083617', '10224682064', '10472181926', '10014893674', '10410764143', '10439021221', '10175504881', '10443130158', '10052519468', '10011704013', '10090660409', '10465646191', '10451402850', '10480050440', '10176300740', '10432089580', '20603958137', '10192188330', '10452624678', '10705836791', '10432776277', '10727781132', '10024304057', '10074421461', '20566455944', '10481031643', '10436592022', '10765649566', '10465268366', '10719739631', '10741233679', '10062855059', '20504137644', '10096308537', '10402425402', '10071201037', '10333204695', '10255693625', '10100152679', '20547891903', '10002081551', '10446721319', '10104419530', '10106943546', '10167376351', '20603809549', '10409063778', '20522050009', '10083898912', '20603190751', '10439426123', '10322896153', '10466950969', '10400458621', '10239865971', '20600702701', '10072832405', '10220793562', '20610042105', '10215604204', '10069408597', '10156901909', '10195712404', '10403345216', '10444194117', '10746523250', '10447327657', '20509994839', '10765672568', '10771319586', '10465117261', '10104029588', '10737617756', '10293520823', '20607663557', '10086143670', '10722792683', '10412834971', '10035967759', '10476684914', '10082580285', '10744142399', '10735455376', '10102082538', '20136649869', '10253316603', '10701514551', '20362906505', '20604978000', '10453371862', '10445344244', '10472898375', '10063013850', '10412760137', '10033834298', '10736736441', '10738105872', '20504850057', '10293523032', '10405989447', '10700051531', '10728854753', '10705508599', '10443654467', '10072326305', '10707733239', '10449922005', '20396134684', '20605249664', '20512886702', '10076102240', '20603111673', '10451529281', '10438963702', '20600980018', '10413602306', '10485523991', '10254577541', '20610200746', '10258140279', '10478284611', '20477455949', '10425749795', '10415953157', '10479150368', '10710312864', '10803586930', '10443489636', '10722324540', '10419518951', '10088110451', '10020244114', '10460095056', '10256614711', '10426022791', '10728385656', '10257880007', '10090445702', '10036413056', '10406557753', '10412426164', '10075419665', '20600166108', '10225024273', '10742078472', '10224149897', '10025543934', '10400429630', '10074426978', '10739618911', '10107565260', '10468330631', '10004381225', '10316615738', '10094287770', '10409920719', '10704716848', '10408953214', '10443921082', '10434050796', '10418367828', '10437540255', '20602478565', '20600521528', '10049611418', '10311831807', '10230021801', '10098708532', '10453076071', '10484749146', '10413309803', '10738033588', '10239913968', '10441771059', '10277452672', '10443164702', '10056449260', '10701416045', '10423022421', '10078530591', '10310425902', '10465539467', '10475671614', '10238941551', '20510370148', '10026106422', '10095593793', '10457868567', '10194342816', '10473294961', '10747317785', '10730127362', '10293164547', '10706177391', '10812467528', '10005011154', '10103087363', '10449227447', '10209916946', '15602933234', '10007924700', '10334294558', '10739903951', '10727103053', '10737668938', '20544767012', '10485816289', '10419394781', '10073140451', '10200989002', '10457563855', '10443642566', '10475880639', '10703984415', '10462938506', '10323857127', '10478066312', '10485861365', '10211221742', '10458773756', '10740491046', '10074602270', '10772365051', '10036169708', '10167630311', '10741273671', '10258627194', '10094947621', '20564253571', '10442358619', '20502309961', '10217928619', '10416109589', '10316193841', '10402969097', '10426475338', '15606956255', '10035860857', '10161210001', '10215346841', '10046422339', '10709811075', '10464577641', '10008397461', '10081541740', '10805844812', '10467447021', '10704480259', '10701176575', '10092216433', '10070836977', '20607960080', '15604271760', '10726654455', '10104832062', '10804918375', '10805657796', '20100505453', '10401119847', '10707399142', '10423428479', '10761507431', '10729273827', '20526481730', '10768792424', '10467396621', '10716024259', '10440357640', '10159608048', '20568726040', '10281000875', '10406343168', '20477447172', '20568214901', '10712788246', '10200393495', '10456255391', '10431484981', '10096779394', '15415979093', '10052490249', '10100821465', '10806289839', '10028906949', '10013016301', '20553733881', '10167184222', '10036097138', '20451412681', '10035614724', '10440507927', '10294206332', '10255848629', '10086034340', '10089963490', '10727646952', '10737693258', '10026110357', '10450232209', '10076709217', '10408531841', '15526962831', '10004894290', '10720732314', '10707884776', '10243672126', '10407829226', '10430469407', '10243844831', '10181402712', '20600974590', '10451437840', '10272693761', '20527555907', '10467464375', '10747636104', '10432506148', '10405123695', '10157619832', '10017683565', '10403067135', '10752611098', '10180683785', '10445200897', '10477309530', '10446925577', '20445564134', '10267017765', '10093470015', '10745350271', '20338739053', '10709696357', '10731862309', '10277482644', '10482892898', '10733209076', '10746625346', '10429004034', '20521263718', '10750659956', '10702081420', '10464805139', '10012100804', '10004698920', '10052298658', '10452156151', '10088266809', '20603256795', '10433223000', '10451003441', '10269625983', '10224209831', '10746293513', '10232146988', '10181127762', '10093655643', '10016859716', '10458305159', '10473083642', '10103780832', '10199192006', '10222877747', '10464948649', '10751209041', '10405409564', '10416218116', '10476347489', '10713388730', '10703568993', '10416847059', '10068589245', '10044179909', '10404367469', '10188439654', '10402943390', '10102247740', '10402875831', '20534659432', '10700200219', '10463603826', '10068410369', '10235564381', '10726916654', '10769916941', '10440776031', '10028450929', '10447973168', '10803408039', '20119180261', '10446264988', '10082558581', '10408564994', '10062367445', '20448431291', '10195652274', '10455449362', '10159790059', '10435104776', '10270495864', '10803851307', '10107864178', '10452985115', '20101617204', '17206390832', '10422658951', '10090130183', '10068695916', '20122607331', '10488068542', '20204895962', '10307664866', '10102948713', '10488520046', '10468034579', '10483268080', '10092719281', '10002238905', '10477671719', '10716580194', '10068883585', '10294240018', '20115420004', '10412271420', '10478404005', '10181255922', '10276897336', '10447452168', '10772890511', '10101620684', '10723600958', '10755642806', '10246736711', '10770853236', '10316779391', '10006641097', '20491941708', '10105815897', '10463129652', '10701940470', '20602471323', '10706025591', '10433671576', '15610431183', '10017804729', '10451922314', '10403382839', '10098668174', '10403369751', '10430596441', '10218504936', '20450202585', '10431596046', '10710485432', '10012949109', '10243604490', '10405807136', '10450692498', '10412223701', '10089590537', '20611402709', '10432771232', '20609488833', '10085593604', '10079705131', '10180759340', '10419579527', '10074013142', '10082354081', '10408753762', '20565447981', '10714699615', '20600069862', '10475155411', '10033219097', '10400615107', '10728962459', '10701348597', '10093638528', '10238743295', '10476455583', '10460829581', '20610499911', '10076338898', '10412865427', '10258451878', '10079952236', '10723087894', '10727786894', '20611084987', '10700187387', '10338020509', '10027448718', '10409529335', '10026182293', '10727050138', '10706818541', '10098262437', '10441873234', '10401677211', '10414593246', '10756010064', '10215784067', '10071498706', '10704677583', '10082545781', '10238180215', '10105172945', '10418441734', '10716079606', '10700240971', '10483807941', '10451437106', '10218668556', '10329211351', '10707590578', '10429139398', '20600809637', '20604689237', '10071832487', '10073664981', '10724525020', '10476476394', '10473890521', '10077185823', '10255254664', '10610398451', '10436274616', '10769429544', '10444120202', '10465357423', '10701309958', '10423859771', '10467542627', '20310203522', '10107417228', '10427999721', '20606378077', '10295977189', '10426742361', '10065851062', '20335736428', '10714735158', '10455488830', '10730928730', '10017039518', '20610231625', '10715250395', '15122628849', '10293334329', '10097353749', '10414001802', '10619641243', '10238340620', '20604911835', '10731287304', '10295188630', '10218632934', '10739845322', '20608677772', '10740246572', '10156331355', '10073939700', '10714579342', '10708308493', '10336542613', '10732133190', '15606818626', '10773394321', '10053122286', '10254519290', '10414202352', '10324807395', '10158454713', '10409662418', '10460946757', '10200675253', '10053564050', '10445450851', '10746965384', '20601992303', '10235266747', '10089896318', '10461141833', '10316302225', '10478738230', '20101826385', '10198187611', '10422372674', '10296771371', '20529463953', '10424191197', '10718195671', '10705201639', '10436496422', '10047488384', '10749057331', '10028101967', '10074830655', '10407363600', '10215353023', '10038323097', '10178413142', '10103006622', '10489520848', '10022819963', '10404427372', '10462698483', '10755859414', '10258474452', '10107915015', '10230059344', '10086877592', '10255464588', '10415778002', '10073256611', '10400636813', '10272546300', '10167840171', '20534536942', '20608798405', '10424582765', '10167966786', '10458290755', '10095147963', '10238138880', '10405305301', '10741506349', '10464179211', '10316161397', '10737875577', '10776892659', '10428439894', '10099855628', '10324802369', '10449962384', '10162974055', '10415777260', '10745485851', '20603545479', '10771179130', '10480392961', '10428027472', '10000055498', '10722525944', '10292011054', '10095036444', '10466874936', '10192270621', '10062561519', '17116899574', '10083054633', '10462874761', '20479846619', '10218518261', '10747301617', '15416964511', '10479066847', '10425425221', '10457080064', '10335928089', '10073015753', '10415326632', '10442878604', '20392688502', '10441018440', '10180301521', '10422544530', '10465030408', '10626026601', '20565820371', '10089908731', '10189863751', '10476809440', '10802063071', '20608200755', '10165901997', '10253108342', '10070070648', '10100558233', '20602665187', '20600820291', '10461875730', '10255396914', '10062345981', '15607682418', '10210890420', '10802359972', '10224120147', '10102469483', '10010435060', '10082914256', '10296777574', '20552538898', '10096675505', '10471246013', '10461750163', '10436218309', '10731418221', '10101699027', '10464383781', '10071754567', '20610199926', '20566113989', '10222772236', '10181919324', '10092700068', '10404266999', '10069423928', '10404020647']


response_times = []
for value in values:
    new_url = url + value
    start_time = time.time()
    response = requests.get(url=new_url)
    end_time = time.time()
    response_time = end_time - start_time
    response_times.append(response_time)
    print(f"Response time for value {value}: {response_time} seconds")

average_time = sum(response_times) / len(response_times)
max_time = max(response_times)
print(f"Average response time: {average_time} seconds")
print(f"Maximum response time: {max_time} seconds")