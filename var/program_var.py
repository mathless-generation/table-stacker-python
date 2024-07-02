from typing import Dict


FILE_TYPE_DICT: Dict = {
    1: { 
        "type": "CSV", 
        "extension": [".csv"]
    }, 
    2: {    
        "type": "Excel", 
        "extension": [".xls"] 
    }, 
    3: { 
        "type": "CSV and Excel", 
        "extension": [".csv", ".xls"] 
    }, 
    4: { 
        "type": "PDF", 
        "extension": [".pdf"] 
    }
} 