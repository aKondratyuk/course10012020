from dal.credentials import BASE, USERNAME, PASSWORD, HOST, PORT, DATABASE

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#db_string = 'postgres://zmgkgurjxpvvwy:e89d9a4d4a2e10b33d5b34dedc14ddd167f0a2e597a43af6bd398cfad8086e8b@ec2-79-125-2-142.eu-west-1.compute.amazonaws.com:5432/da83mg4ouf002p'
#db_string = "postgresql://localhost/image2code"  #user=andrii
db_string = 'postgres://zshiupzueytehw:d19451e5fd87df2b1170609fb1ac7d69796b2e29ef352ebfdee3c59ddd9923ed@ec2-54-247-170-5.eu-west-1.compute.amazonaws.com:5432/d5japvloj4nrnr'
#db_string = '{base}://{user}:{pw}@{host}:{port}/{db}'.format(base=BASE,user=USERNAME,pw=PASSWORD,host=HOST,port=PORT,db=DATABASE)

engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()

metadata = Base.metadata
