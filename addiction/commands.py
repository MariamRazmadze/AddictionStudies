from flask.cli import with_appcontext
import click
from addiction.extensions import db
from addiction.models.staff import Staff
from addiction.models.user import User, UserRole, Role
from addiction.models.home import Home
from addiction.models.projects import Project
from flask import current_app
from addiction.models.file import File
import os
import csv
from csv import reader, DictReader
import pprint

@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Finished Creating Database")


@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating staff")
    
    # fields=['name', 'email', 'position']
    # s=[{"name": "ჯანა ჯავახიშვილი", "email":"darejan.javakhishvili@iliauni.edu.ge","position":"ილიაუნის ადიქტოლოგიის ინსტიტუტის დირექტორი და მკვლევარი, ფსიქოლოგიურ მეცნიერებათა დოქტორი, ილიაუნის მეცნიერებათა და ხელოვნების ფაკულტეტის პროფესორი; საქართველოს ადიქტოლოგთა ასოციაცის თანადამფუძნებელი და გამგეობის წევრი; ტრავმული სტრესის კვლევის საერთაშორისო საზოგადოების (ISTSS) დირექტორთა საბჭოს წევრი"},
    #    {"name": "დავით ოთიაშვილი", "email":"davit.otiashvili@iliauni.edu.ge", "position":"ილიაუნის ადიქტოლოგიის ინსტიტუტის თანადამფუძნებელი და მკვლევარი, ჯანმრთელობის ფსიქოლოგიის დოქტორი, ილიაუნის სამედიცინო სკოლის ასოცირებული პროფესორი, საქართველოს ადიქტოლოგთა ასოციაციის თავმჯდომარე, საქართველოს ნარკომანიასთან ბრძოლის უწყებათაშორისი საბჭოს წევრი, სადაც წარმოადგენს არასამთავრობო სექტორს"},
    #    {"name": "ირმა კირთაძე","email":"irma.kirtadze@iliauni.edu.ge", "position":"ილიაუნის ადიქტოლოგიის ინტიტუტის თანადამფუძმნებელი და მკვლევარი, საზოგადოებრივი ჯანმრთელობის დოქტორი, ილიაუნის მეცნიერებათა და ხელოვნების ფაკულტეტის ასოცირებული პროფესორი, საქართველოს ადიქტოლოგთა ასოციაციის თანადამფუძნებელი და გამგეობის წევრი"}, 
    #    {"name":"მარიამ რაზმაძე","email":" mariam.razmadze.3@iliauni.edu.ge", "position":"ილიაუნის ადიქტოლოგიის ინსტიტუტის კოორდინატორი და მკვლევარი, ფსიქიკური ჯანმრთელობის მაგისტრი, საქართველოს ადიქტოლოგთა ასოციაცის წევრი, ევროპის პრევენციის კურიკულუმის ეროვნული ტრენერი"}]
    

    # with open (os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'staff.csv'), mode='w') as staff_csv:
    #     writer=csv.DictWriter(staff_csv, fieldnames=fields)
    #     writer.writeheader()
    #     writer.writerows(s)
    
    path=os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'staff.csv')
    with open(path, "r") as staff_csv:
        csv_reader= csv.DictReader(staff_csv)
        for row in csv_reader:
            new_member = Staff(name=row['name'], email=row['email'], position=row['position'])
            new_member.create()
    


    click.echo("Creating users")
    admin_user=User(username="admin1", password='asdf', email='admin@gmail.com')
    admin_user.create()

    roles=['user', 'moderator', 'admin']
    for role in roles:
        new_role=Role(name=role)
        new_role.create()
    
    admin_role=Role.query.filter_by(name="admin").first()
    admin_user_role=UserRole(user_id=admin_user.id, role_id=admin_role.id)
    admin_user_role.create()


    click.echo("Creating files")
    path=os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'file.csv')
    with open(path, "r") as file_csv:
        csv_reader= csv.DictReader(file_csv)
        for row in csv_reader:
            new_file = File(filename=row['filename'], displayname=row['displayname'], category=row['category'], folder=row['folder'])
            new_file.create()
    
    fields=['displayname', 'filename',  'category', 'folder']
    f=[{"displayname":"ყურადღების ცენტრში: ფენტანილები და სხვა ახალი ოპიოიდები", 
        "filename": "10 Spotlight on... Fentanyls and other new opioids_GEO_29.11.22.pdf", 
        "category": "ფსიქოგანათლება", "folder":"psychoed"}, 
        {"displayname": "ყურადღების ცენტრში: სინთეზური კანაბინოიდები", 
         "filename": "09 Spotlight on... Synthetic Cannabinoids_GEO_29.11.22.pdf", 
         "category": "ფსიქოგანათლება", "folder":"psychoed"}, 
        {"displayname":"ყურადღების ცენტრში: ფსიქოაქტიური ნივთიერებების მოხმარება და ფსიქიკური ჯანმრთელობის კომორბიდული პრობლემები", 
          "filename":"12 Spotlight on... Comorbid substance use and mental health problems_GEO_29.11.22.pdf", 
          "category": "ფსიქოგანათლება", "folder":"psychoed"}, 
        {"displayname": "ხარისხის სტანდარტების დანერგვა ნარკოლოგიური სერვისებისა და სისტემებისთვის", 
         "filename":"07 Implementing quality standards for drug services and systems_GEO_29.11.22.pdf", 
         "category": "წიგნები", "folder":"books"
         }, 
        {"displayname": "ნარკოტიკების ავადმოხმარების პრევენცია", 
         "filename":"ნარკოტიკების ავადმოხმარების პრევენციის სახელმძღვანელო - 2017-2.pdf", 
        "category": "წიგნები", "folder":"books"}, 
        {"displayname":"სამოქმედო ჩარჩო ნარკოტიკებთან დაკავშირებულ პრობლემებზე საპასუხო ჯანდაცვითი და სოციალური ზომების შემუშავებისა და განხორციელებისთვის", 
         "filename":"01 Action Framework GEO_29.11.22 .pdf", 
         "category": "წიგნები", "folder":"books"}, 
        {"displayname": "მედია, ფსიქიკური ჯანმრთელობა და ადამიანის უფლებები", 
         "filename": "მედია, ფსიქიკური ჯანმრთელობა და ადამიანის უფლებები-ჯანა ჯავახიშვილი Final.pdf", 
         "category": "წიგნები", "folder":"books"}, 
         {"displayname": "კანაფი: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
          "filename":"02 Cannabis GEO_28.11.22.pdf", 
          "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
        {"displayname":"ოპიოიდები: ჯანდაცვითი და სოციალური საპასუხო ზომები",
         "filename":"11 Opioids health and social responses_GEO_28.11.22.pdf", 
         "category": "მკურნალობის გზამკვლევები", "folder":"treatment"},  
        {"displayname":"ახალი ფსიქოაქტიური ნივთიერებები: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
         "filename":"03 New psychoactive substances health and social responses_GEO_28.11.22.pdf", 
         "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
         {"displayname":"სტიმულატორები: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
          "filename":"05 Stimulants health and social responses_GEO_28.11.22.pdf", 
          "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
        {"displayname":"ოპიოიდების მოხმარებასთან დაკავშირებული სიკვდილი: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
         "filename":"08 Opioid-related deaths health and social responses_GEO_28.11.22.pdf", 
         "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
        {"displayname":"წამლების არასამედიცინო დანიშნულებით გამოყენება: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
         "filename":"06 Non-medical use of medicines health and social responses_GEO_28.11.22.pdf", 
         "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
        {"displayname":"ნარკოტიკების პოლიმოხმარება: ჯანდაცვითი და სოციალური საპასუხო ზომები", 
         "filename":"04 Polydrug use health and social responses_GEO_28.11.22.pdf", 
         "category": "მკურნალობის გზამკვლევები", "folder":"treatment"}, 
        {"displayname":"Piloting Comprehensive Social Influence (‘Unplugged’) Program in Georgia: A", 
         "filename":"Pilot of Uplugged Program in Georgia.pdf", 
         "category":"აკადემიური პუბლიკაციები", "folder":"academic"}, 
        {"displayname":"‘Ten Years Later’ – Developing Institutional Mechanisms for Drug Demand Reduction and Addictology Education in Georgia – A Case Study", 
         "filename":"addictology development in georgia - javakhishvili, otiashvili, kirtaedze, 2022.pdf", 
         "category":"აკადემიური პუბლიკაციები", "folder":"academic"}, 
        {"displayname":"ჩანაცვლებითი თერაპიის სერვისებით მოსარგებლეთა კმაყოფილების კვლევა დასავლეთ საქართველოში", 
         "filename":"HR-Study-Rep-GEO-May 17.pdf", 
         "category": "კვლევითი ანგარიშები", "folder":"research"}, 
        {"displayname":"პრევენციის ევროპული კურიკულუმი", 
         "filename":"EUPC_GEO_28.11.22_for web.pdf ", 
         "category":"პრევენციის სახელმძღვანელოები", "folder":"prevention"}

    ]   

    # with open (os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'file.csv', ), mode='w', encoding="utf-8", newline="") as file_csv:
    #     writer=csv.DictWriter(file_csv, fieldnames=fields)
    #     writer.writeheader()
    #     for row in f:
    #         writer.writerow({k: f'"{v}"' if "," in str(v) else v for k, v in row.items()})







    click.echo("Creating home")
    
    path=os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'home.csv')
    with open(path, 'r') as home_csv:
        csv_reader= csv.DictReader(home_csv)
        for row in csv_reader:
            new_item= Home(about=row['about'], directions=row['directions'], history=row['history'])
            new_item.create()
    
   
    # d=[{"implemented":"""2013-2015 წლები – პროექტი „The development of human resources, evidence base and quality standards in addictology (trans-disciplinary addiction science) in Georgia“ (ADDIGE). დამფინანსებელი – ევროკომისია, TEMPUS-ის მექანიზმი. პროექტის მთავარი პარტნიორი – ჩარლზის უნივერსიტეტის პირველი სამედიცინო ფაკულტეტის ადიქტოლოგიის დეპარტამენტი. პროექტის ფარგლებში: ამოქმედდა და გაძლიერდა ადიქციის კვლევების სამაგისტრო პროგრამა; შემუშავებულ და აკრედიტებულ იქნა 3-დღიანი პროფესიული დახელოვნების 5 კურსი: ექიმი-ნარკოლოგებისათვის, ექთნებისათვის, სოციალური მუშაკებისათვის, ფსიქოლოგებისათვის, ჟურნალისტებისათვის;
    # ჩატარდა ადიქტოლოგიაში პროფესიული მომზადების 12 კურსი და 3 საზაფხულო სკოლა; ასევე, საზაფხულო სკოლა ახალგაზრდა მეცნიერთათვის ფსიქოტრავმატოლოგიაში ევროპის ტრავმული სტრესის კვლევის საზოგადოებასთან (ESTSS-თან) თანამშრომლობით; მომზადდა და გამოიცა საქართველოს ნარკოვითარების სამი ანალიტიკური ანგარიში (2013, 2014 და 2015 წლების); ჩატარდა საქართველოში მოქმედი ადიქტოლოგიური სტანდარტების კვლევა; განხორციელდა საერთაშორისო ადიქტოლოგიური სტანდარტების კვლევა; 
    # ჩატარდა ახალგაზრდებში ჯანმრთელობასთან დაკავშირებული ქცევის პატერნების კვლევა იზრაელის ბენჰურიონის უნივერსიტეტთან ერთად.""", "current":"2019 წლის აპრილიდან დღემდე (პროექტი გრძელდება 2023 წლის ივნისამდე) – პროექტი „Prevention of Addictions and Mental Disorders Among Adolescents in Georgia” (PAMAD), დონორი: ინგლისის სამედიცინო კვლევების საბჭო (Medical Research Council, UK; MR/S025278/1). პროექტის ფარგლებში ვთანამშრომლობთ ინგლისის მხრიდან – ლონდონის ტროპიკული მედიცინის სკოლასთან (London School of Tropical Medicine) და კარდიფის უნივერისტეტთან (Cardiff University); საქართველოს მხრიდან – ფონდთან „კურაციო“ და ფონდთან „გლობალური ინიციატივა ფსიქიატრიაში-თბილისი“. ფონდი „კურაციო“ არის პროექტის წამყვანი განმახორციელებელი ინსტიტუცია. კერძოდ, ფონდმა გლობალური ინიციატივა ფსიქიატრიაში-თბილისი 2019 წელს დააფუძნა ადიქციის მიზანმიმართული და შერჩევითი პრევენციის ოჯახზე დაფუძნებული სერვისი მოზარდებისთვის „კლუბი სინერგია“, და პროექტის ფარგლებში ამჟამად მიმდინარე კვლეა შეისწავლის სერვისის შედეგიანობას. კვლევის შედეგების საფუძველზე უკვე გამოქვეყნდა ერთი პუბლიკაცია ევროპის ფსიქოტრავმატოლოგიურ ჟურნალში, კიდე ორი პუბლიკაცია მომზადების პროცესშია." }, 
    # {"implemented": "2015-2017 წლები, პროექტი „ტოლერანტობის მარცვლები“. დამფინანსებელი – ევროკომისია (უკრაინა); პროექტის პარტნიორია ლონდონის ტროპიკული მედიცინის სკოლა. პროექტის ფარგლებში ჩატარდა უკრაინაში იძულებით გადაადგილებული პირების რეპრეზენტატიული შერჩევის ფსიქიკური ჯანმრთელობის პრობლემებისა და ალკოჰოლის მოხმარების კვლევა. კვლევის შედეგები ასახულია საერთაშორისო აკადემიურ ჟურნალებში დაბეჭდილ 5 სტატიაში. ", "current": "2020 წლიდან დღემდე – ევროპის ტრავმული სტრესის კვლევის საზოგადოების ADJUST Study. ვახორციელებთ ერთროულად ევროპის 11 ქვეყანაში, ვიკვლევთ (ონალინ გამოკითხვის საშუალებით) კოვიდის პანდემიის გავლენას მოსახლეობის ფსიქიკურ ჯანმრთელობაზე. საქართველოს გუნდი მუშაობს მოხალისეობრივად, საქართველოში ჩატარებული კვლევის ფრაგმენტი ილიაუნის დოქტორანტის სადოქტორო დისერტაციის თემაა. მონაცემთა შესაგროვებელ პლატფორმასა და MAXQDA თვისებრივი ანალიზის პროგრამას აფინანსებს საქართველოს წამების მსხვერპლთა რეაბილიტაციის ცენტრი. პროექტის ფარგლებში გამოქვეყნდა უკვე ხუთი პუბლიკაცია საერთაშორისო რეფერირებად ჟურნალებში და იგეგმება შემდგომი პუბლიკაციები."},  
    # {"implemented": "2016-2017 წლები – პროექტი: „იზრაელის ბენჰურიონის უნივერსიტეტსა და ილიას სახელმწიფო უნივერსიტეტში ჯანმრთელობის სარისკო ქცევებისა და ფსიქოაქტიური საშუალებების მოხმარების გავრცელების კვლევა“. პარტნიორი – იზრაელის ბენჰურიონის უნივერსიტეტი; პროექტი სამოხალისეოდ განხორციელდა. პროექტის ფარგლებში ჩატარდა რეოდენობრივი ონალინ გამოკითხვა ორივე უნივერსიტეტის სტუდენტებისა.", "current": "2021 წლის დეკემბრიდან დღემდე (პროექტი გრძელდება 2023 წლის მარტამდე) – პროექტი „ევროპის პრევენციის კურიკულუმის თარგმნა, ადაპტირება და ფორმატირება საქართველოში“, დამფინანსებელი – ევროპის ნარკოტიკებისა და წამალდამოკიდებულების მონიტორინგის ცენტრი (EMCDDA), განმახორციელებელი: ილიაუნის ადიქტოლოგიის ინსტიტუტი. პროექტის ფარგლებში ითარგმნა ევროპის პრევენციის კურიკულუმის სახელმძღვანელო, ჩატარდა მაფორმატირებელი კვლევა და ამ კვლევის საფუძველზე სახელმძღვანელო იქნა ადაპტირებული."}, 
    # {"implemented":"2017-2020 წლები – პროექტი „აივ-შიდსის პრევენცია ქუჩასთან დაკავშირებულ ბავშვებში“,  დაფინანსებულია შოთა რუსთაველის ეროვნული ფონდის საბაზო კვლევითი სახელმწიფო გრანტების კონკურსის ფარგლებში. პროექტი მიზნად ისახავდა ქუჩასთან დაკავშირებულ ბავშვებში აივ-ის გავრცელების თვალსაზრისით რისკისა და დამცავი ფაქტორების გამოვლენას. პროექტის ფარგლებში გამოიცა წიგნი „ქუჩასთან დაკავშირებული ახალგაზრდები: ეთიკური კვლევა და ანალიტიკა“, სტატიები გამოცემის პროცესშია.", "current": "2022 წლის თებერვლიდან დღემდე (პროექტი გრძელდება 2023 წლის მარტამდე) – პროექტი „ადიქციების მკურნალობის მინი-გზამკვლევების თარგმნა, ადაპტირება და ფორმატირება საქართველოში“, დამფინანსებელი – ევროპის ნარკოტიკებისა და წამალდამოკიდებულების მონიტორინგის ცენტრი (EMCDDA), განმახორციელებელი: ილიაუნის ადიქტოლოგიის ინსტიტუტი. პროექტის ფარგლებში ითარგმნა ევროპის ნარკოტიკებისა და წამალდამოკიდებულების მონიტორინგის ცენტრის მიერ მომზადებული მკურნალობის 12 გზამკვლევი, ჩატარდა მაფორმატირებელი კვლევა და ამ კვლევის საფუძველზე ხორციელდება გზამკვლევების ადაპტაცია."},
    # {"implemented":"2019 წლის აპრილი-დეკემბერი – პროექტი „ნარკომანიის პრევენციისა და ნარკოპოლიტიკის პოლიტიზება საქართველოში“, მხარდაჭერილი ილიაუნის ინსტიტუციური განვითარების საგრანტო კონკურსის ფარგლებში. პროექტის პარტნიორი/კონსულტანტი იყო სირაკუზის უნივერსიტეტის პროფესორი დესსა ბერგენ-სიკო. პროექტის ფარგლებში ჩატარდა საქართველოში განხორციელებული პრევენციული საინფორმაციო კამპანიების ნარატივებისა და დისკურსების თვისებრივი კვლევა."}, 
    # {"implemented": "2019 წელი – პროექტი „ოპიოიდებით ჩანაცვლებითი მკურნალობის ხელმისაწვდომობა საქართველოს პენიტენციურ სისტემაში: არსებული გამოწვევების და ბარიერების შესწავლა“, დაფინანსებელია ქართული არასამთავრობო ფონდის CTC-ი (Center for Training and Consultancy) მიერ, რომელიც თავად იყო ევროკავშირის დაფინანსებული პროექტის განმახორციელებლი და ამ პროექტის ფარგლებში ჩაატარა კვლევითი გრანტების კონკურსი, რომლის ფარგლებშიც გაიმარჯვა ილიაუნის ადიქტოლოგიის ინსტიტუტის განაცხადმა. პროექტის ფარგლებში ჩატარდა თვისებრივი კვლევა ყოფილ პატიმრებთან და ექსპერტთა ფოკუს ჯგუფები."}, 
    # {"implemented": "2020-2021 წლები – პროექტი „ოპიოიდებით ჩანაცვლებითი თერაპიის სერვისებით მოსარგებლეთა კმაყოფილების კვლევა დასავლეთ საქართველოში“, დამფინანსებელი ევრაზიის ზიანის შემცირების ასოციაცია (EAHRA), განმახორციელებელი ილიაუნის ადიქტოლოგიის ინსტიტუტი; წამყვანი განმახორციელებლი ინსტიტუცია – ფონდი „გლობალური ინიციატივა ფსიქიატრიაში – თბილისი“. პროექტის ფარგლებში ჩატარდა დასავლეთ საქართველოში ოპიოიდებით ჩანაცვლებითი თერაპიის სერვისებში ჩართულ მოსარგებლეთა წარმომადგენლობითი შერჩევის გამოკითხვა. კველვის ანგარიში გამოქვეყნდა ქართულ და ინგლისურ ენებზე; პუბლიკაცია საერთაშორისო სამეცნიერო ჟურნალისთვის მომზადების პროცესშია."},


    # ]
        # fields=['implemented', 'current']
    # with open (os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'projects.csv'), mode='w') as projectin_csv:
    #     writer=csv.DictWriter(projectin_csv, fieldnames=fields)
    #     writer.writeheader()
    #     writer.writerows(d)
    

    click.echo("Creating Projects")

    path=os.path.join(current_app.config['BASE_DIR'], 'csvfiles', 'projects.csv')
    with open(path, 'r') as projects_csv:
        csv_reader= csv.DictReader(projects_csv)
        for row in csv_reader:
            new_project= Project(current=row['current'], implemented=row['implemented'])
            new_project.create()



    



