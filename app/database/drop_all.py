from app.database import engine, Base
import sqlalchemy as sa
from app.models import * 

def drop_everything():
    
    with engine.begin() as conn:
        conn.execute(sa.text("DROP VIEW IF EXISTS vw_excersice_details CASCADE"))
        
    Base.metadata.drop_all(bind=engine)
    
    with engine.begin() as conn:
        conn.execute(sa.text("DROP TABLE IF EXISTS alembic_version CASCADE"))
    

if __name__ == "__main__":
    drop_everything()
