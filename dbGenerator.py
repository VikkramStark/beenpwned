from app import WordList, db, app 
import os 
from sqlalchemy.exc import IntegrityError 
from multiprocessing import Process, current_process 

files = os.listdir("wordlists") 
# print(files) 


app.app_context().push() 
db.create_all() 
# db.session.rollback() 


lines = open(os.path.join("wordlists","rockyou.txt"), "r", errors="ignore").read().split("\n")

n_lines = len(lines)
half_size = n_lines//2 
quater_size = n_lines//4 

# for file in files:
#     fullpath = os.path.join(".","wordlists",file) 
#     lines = open(fullpath, "r", errors="ignore").read().split("\n")  
#     count = 0 
    # for word in lines:
    #     try:
    #         newWord = WordList(word = word) 
    #         db.session.add(newWord)   
    #         count += 1    
    #         db.session.commit()
    #         print("Added", word)
    #         if count >=1000:
    #             print("Committing Database!!")  
    #             count = 0 

    #     except IntegrityError:
    #         db.session.rollback() 
    #         print(f"Skipping...{word}")    
    #         continue 
        
        # except Exception as e: 
        #     if e!=IntegrityError:
        #         db.session.rollback()
        #         print("Error Adding Word", word, "\n Rolling Back!!...")   
        #         print(e) 
        #         break 


def add_word_to_db(lines):
    for word in lines:
        try:
            res = WordList.query.filter_by(word = word).all() 
            if res == []: 
                newWord = WordList(word = word) 
                db.session.add(newWord)   
                # count += 1    
                db.session.commit()
                print("Added", word) 
            # if count >=1000:
            #     print("Committing Database!!")  
            #     count = 0 

        except Exception as e: 
            db.session.rollback() 
            print(f"Skipping...{word}")    
            break 
        
        # except Exception as e: 
        #     if e!=IntegrityError:
        #         db.session.rollback()
        #         print("Error Adding Word", word, "\n Rolling Back!!...")   
        #         print(e) 
        #         break 

#Change these Lines Accordingly to cover whole list for paralle processing 

p1 = Process(target = add_word_to_db, args = (lines[:quater_size],))  
p2 = Process(target = add_word_to_db, args = (lines[quater_size: half_size],)) 
p3 = Process(target = add_word_to_db, args = (lines[half_size:half_size+quater_size],))            
p4 = Process(target = add_word_to_db, args = (lines[-quater_size:],))  


 

if __name__ == "__main__":
    
    p1.start() 
    p2.start()
    p3.start()
    p4.start()  
   

    p1.join() 
    p2.join() 
    p3.join() 
    p4.join() 


 
     

