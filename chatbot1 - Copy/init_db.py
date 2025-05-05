from pymongo import MongoClient
import json

# MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://jpatil2670:6260162831@cluster0.bi5q8.mongodb.net/teerth-saarthi?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['teerth-saarthi']
places_collection = db['places']

# Clear existing data
places_collection.drop()

# Sample data for religious places
sample_places = [
    {
        "name": "Golden Temple",
        "type": "temple",
        "religion": "Sikhism",
        "history": "The Golden Temple, also known as Sri Harmandir Sahib, was founded in 1589 by Guru Arjan, the fifth Sikh Guru. The temple was built as a place of worship for all people, regardless of religion or background. The foundation stone was laid by a Muslim saint Hazrat Mian Mir. The temple was rebuilt after being destroyed several times during attacks in the 18th century.",
        "location": {
            "address": "Golden Temple Rd, Amritsar, Punjab 143006, India",
            "description": "Located in the heart of Amritsar, Punjab, India."
        },
        "nearby_attractions": [
            "Jallianwala Bagh",
            "Wagah Border",
            "Partition Museum",
            "Gobindgarh Fort",
            "Maharaja Ranjit Singh Museum"
        ],
        "transportation": {
            "air": "Nearest airport is Sri Guru Ram Dass Jee International Airport (13 km away, approximately Rs. 400-600 by taxi)",
            "train": "Amritsar Junction Railway Station (3 km away, well-connected to major cities)",
            "bus": "Amritsar Bus Terminal (2 km away, regular services from Punjab and neighboring states)",
            "local": "Auto-rickshaws (Rs. 100-150) and cycle-rickshaws (Rs. 50-100) are available"
        },
        "accommodations": [
            {
                "name": "Golden Temple Free Accommodation",
                "type": "Free Dormitory",
                "price_range": "Free"
            },
            {
                "name": "Hotel Hong Kong Inn",
                "type": "Budget Hotel",
                "price_range": "Rs. 1,000-2,000 per night"
            },
            {
                "name": "Golden Tulip Amritsar",
                "type": "Luxury Hotel",
                "price_range": "Rs. 3,000-5,000 per night"
            },
            {
                "name": "SGPC Rooms",
                "type": "Dharmashala",
                "price_range": "Rs. 100-500 per night"
            }
        ]
    },
    {
        "name": "Varanasi",
        "type": "city",
        "religion": "Hinduism",
        "history": "Varanasi, also known as Kashi or Benares, is one of the oldest continuously inhabited cities in the world, dating back to the 11th century BCE. It is considered the spiritual capital of India and has been a cultural and religious center for thousands of years. The city is particularly sacred to Hindus and Jains and is also an important site in the development of Buddhism.",
        "location": {
            "address": "Varanasi, Uttar Pradesh, India",
            "description": "Located on the banks of the River Ganges in Uttar Pradesh, India."
        },
        "nearby_attractions": [
            "Kashi Vishwanath Temple",
            "Dashashwamedh Ghat",
            "Sarnath",
            "Ramnagar Fort",
            "Assi Ghat",
            "Manikarnika Ghat"
        ],
        "transportation": {
            "air": "Lal Bahadur Shastri International Airport (25 km from city center, approximately Rs. 600-800 by taxi)",
            "train": "Varanasi Junction/Varanasi Cantt railway stations (well-connected to major cities)",
            "bus": "Varanasi has regular bus services from cities in Uttar Pradesh and neighboring states",
            "local": "Auto-rickshaws (Rs. 100-200), cycle-rickshaws (Rs. 50-100), and boat rides on the Ganges (Rs. 100-500)"
        },
        "accommodations": [
            {
                "name": "Kashi Atithi Griha",
                "type": "Dharmashala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Ganga Fuji Home",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            },
            {
                "name": "Taj Ganges",
                "type": "Luxury Hotel",
                "price_range": "Rs. 5,000-10,000 per night"
            },
            {
                "name": "Shri Kashi Vishwanath Dharamshala",
                "type": "Dharmashala",
                "price_range": "Rs. 200-600 per night"
            }
        ]
    },
    {
        "name": "Ajmer Sharif",
        "type": "dargah",
        "religion": "Islam",
        "history": "The Ajmer Sharif Dargah is a Sufi shrine of the revered saint, Moinuddin Chishti, located in Ajmer, Rajasthan. The shrine was built in the 13th century and is visited by thousands of pilgrims every day, regardless of their religious beliefs. It's one of the most sacred pilgrimage sites for Muslims in India and is known for its role in promoting harmony between different faiths.",
        "location": {
            "address": "Dargah Sharif, Ajmer, Rajasthan 305001, India",
            "description": "Located in the city of Ajmer in Rajasthan, India."
        },
        "nearby_attractions": [
            "Ana Sagar Lake",
            "Taragarh Fort",
            "Adhai Din Ka Jhonpra",
            "Mayo College",
            "Pushkar (only 15 km away)"
        ],
        "transportation": {
            "air": "Nearest airport is Jaipur International Airport (130 km away, approximately Rs. 2,000-3,000 by taxi)",
            "train": "Ajmer Junction Railway Station (3 km away, well-connected to major cities)",
            "bus": "Ajmer has regular bus services from cities in Rajasthan and neighboring states",
            "local": "Auto-rickshaws (Rs. 80-150) and taxis are available for local transport"
        },
        "accommodations": [
            {
                "name": "Dargah Inn",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            },
            {
                "name": "Hotel Ajmer Inn",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Ajmer Sharif Guest House",
                "type": "Dharmashala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Railway Retiring Rooms",
                "type": "Budget Accommodation",
                "price_range": "Rs. 500-1,000 per night"
            }
        ]
    },
    {
        "name": "Vatican City",
        "type": "city",
        "religion": "Christianity",
        "history": "Vatican City, officially the Vatican City State, is the smallest country in the world and the headquarters of the Roman Catholic Church. It was established as an independent state in 1929 by the Lateran Treaty between the Holy See and Italy. The Vatican has been the residence of the Pope since 1377 and houses numerous significant religious and cultural sites including St. Peter's Basilica and the Sistine Chapel.",
        "location": {
            "address": "Vatican City, Rome, Italy",
            "description": "Located within the city of Rome, Italy."
        },
        "nearby_attractions": [
            "St. Peter's Basilica",
            "Vatican Museums",
            "Sistine Chapel",
            "Castel Sant'Angelo",
            "Roman Forum",
            "Colosseum"
        ],
        "transportation": {
            "air": "Nearest airport is Rome Fiumicino Airport (30 km away, approximately €50 by taxi)",
            "train": "Roma S. Pietro Railway Station (10-15 minute walk from Vatican)",
            "bus": "Multiple bus lines from central Rome stop near Vatican City",
            "metro": "Line A stops at Ottaviano-San Pietro and Cipro stations (10-15 minute walk to Vatican)"
        },
        "accommodations": [
            {
                "name": "Hotel della Conciliazione",
                "type": "Mid-range Hotel",
                "price_range": "€80-150 per night"
            },
            {
                "name": "Vatican Guest House",
                "type": "Budget Hotel",
                "price_range": "€50-100 per night"
            },
            {
                "name": "Residenza Paolo VI",
                "type": "Luxury Hotel",
                "price_range": "€150-300 per night"
            },
            {
                "name": "Casa Tra Noi",
                "type": "Religious Guest House",
                "price_range": "€60-120 per night"
            }
        ]
    },
    {
        "name": "Bodhgaya",
        "type": "temple",
        "religion": "Buddhism",
        "history": "Bodhgaya is the place where Gautama Buddha attained enlightenment under the Bodhi Tree. It is located in the Gaya district of Bihar, India. The Mahabodhi Temple Complex, which includes the sacred Bodhi Tree, is a UNESCO World Heritage Site and one of the four holy sites related to the life of the Buddha. The original temple was built by Emperor Ashoka in the 3rd century BCE, with the current temple dating back to the 5th-6th centuries CE.",
        "location": {
            "address": "Bodhgaya, Bihar 824231, India",
            "description": "Located in the Gaya district of Bihar, India."
        },
        "nearby_attractions": [
            "Mahabodhi Temple",
            "Bodhi Tree",
            "Great Buddha Statue",
            "Thai Temple",
            "Japanese Temple",
            "Tibetan Monastery"
        ],
        "transportation": {
            "air": "Nearest airport is Gaya International Airport (17 km away, approximately Rs. 400-600 by taxi)",
            "train": "Gaya Junction Railway Station (16 km away, well-connected to major cities)",
            "bus": "Regular bus services from Patna and other cities in Bihar",
            "local": "Auto-rickshaws (Rs. 100-200) and cycle-rickshaws (Rs. 50-100) are available"
        },
        "accommodations": [
            {
                "name": "Root Institute",
                "type": "Buddhist Retreat Center",
                "price_range": "Rs. 500-1,500 per night"
            },
            {
                "name": "Hotel Bodhgaya Regency",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Mahamaya Hotel",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            },
            {
                "name": "Burmese Vihar",
                "type": "Monastery Guesthouse",
                "price_range": "Rs. 300-800 per night or donation basis"
            }
        ]
    },
    {
        "name": "Somnath Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "The Somnath Temple, located in Prabhas Patan, Gujarat, is one of the most sacred pilgrimage sites for Hindus and the first among the twelve Jyotirlinga shrines of Lord Shiva. The temple has been destroyed and rebuilt several times throughout history. The current structure was built in 1947 after India's independence. According to historical records, the original temple was built in gold by the Moon God (Soma), rebuilt in silver by Ravana, in wood by Krishna, and in stone by Bhimdev. The temple was repeatedly destroyed by various invaders, including Mahmud of Ghazni in 1024 CE, Alauddin Khilji in 1298, and Aurangzeb in 1665. Each time, it was rebuilt by devoted Hindu rulers and devotees.",
        "location": {
            "address": "Somnath Temple, Somnath Mandir Rd, Prabhas Patan, Somnath, Gujarat 362268, India",
            "description": "Located on the western coast of Gujarat, overlooking the Arabian Sea."
        },
        "nearby_attractions": [
            "Somnath Beach",
            "Bhalka Tirth",
            "Triveni Sangam",
            "Dehotsarg Teerth",
            "Junagadh Gate",
            "Somnath Museum"
        ],
        "transportation": {
            "air": "Nearest airport is Diu Airport (63 km away) or Rajkot Airport (180 km away)",
            "train": "Veraval Railway Station (7 km away) is the nearest railway station",
            "bus": "Regular bus services from major cities in Gujarat to Somnath Bus Station",
            "local": "Auto-rickshaws and taxis available for local transport (Rs. 100-200)"
        },
        "accommodations": [
            {
                "name": "Somnath Trust Dharamshala",
                "type": "Dharmashala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Lords Inn Somnath",
                "type": "Luxury Hotel",
                "price_range": "Rs. 3,000-5,000 per night"
            },
            {
                "name": "Hotel Sudarshan",
                "type": "Budget Hotel",
                "price_range": "Rs. 1,000-2,000 per night"
            },
            {
                "name": "GTDC Resort Somnath",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            }
        ]
    },
    {
        "name": "Mehandipur Balaji Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Mehandipur Balaji Temple is a famous temple dedicated to Lord Hanuman, located in Rajasthan. It is known for its unique rituals and is believed to cure people possessed by evil spirits. The temple was built in a distinctive architectural style and attracts thousands of devotees daily.",
        "location": {
            "address": "Mehandipur Balaji Temple, Dausa, Rajasthan 321609, India",
            "description": "Located in Dausa district of Rajasthan, approximately 80 km from Jaipur."
        },
        "nearby_attractions": [
            "Kaila Devi Temple",
            "Galtaji Temple",
            "Chand Baori",
            "Abhaneri Step Well",
            "Bhandarej"
        ],
        "transportation": {
            "air": "Nearest airport is Jaipur International Airport (95 km away)",
            "train": "Nearest railway station is Bandikui Junction (25 km away)",
            "bus": "Regular bus services from Jaipur and other major cities in Rajasthan",
            "local": "Taxis and auto-rickshaws available from nearby towns"
        },
        "accommodations": [
            {
                "name": "Balaji Temple Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Hotel Balaji Palace",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            },
            {
                "name": "Mehandipur Guest House",
                "type": "Guest House",
                "price_range": "Rs. 500-1,000 per night"
            }
        ]
    },
    {
        "name": "Mahakaleshwar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Mahakaleshwar Temple is one of the twelve Jyotirlingas and is located in Ujjain, Madhya Pradesh. The temple is situated on the banks of the Shipra River and is believed to be built in the 6th century CE. The temple's current structure was built by the Maratha ruler Ranoji Shinde in 1736 CE.",
        "location": {
            "address": "Jaisinghpura, Ujjain, Madhya Pradesh 456006, India",
            "description": "Located in the ancient city of Ujjain, Madhya Pradesh."
        },
        "nearby_attractions": [
            "Ram Ghat",
            "Kal Bhairav Temple",
            "Harsiddhi Temple",
            "Mangalnath Temple",
            "Gopal Mandir"
        ],
        "transportation": {
            "air": "Nearest airport is Devi Ahilyabai Holkar Airport, Indore (55 km away)",
            "train": "Ujjain Junction Railway Station (2 km away)",
            "bus": "Ujjain Bus Stand with regular services to major cities",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "Mahakal Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Shipra Residency",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Ujjain Palace Hotel",
                "type": "Luxury Hotel",
                "price_range": "Rs. 3,000-6,000 per night"
            }
        ]
    },
    {
        "name": "Amarnath Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "The Amarnath Temple is a Hindu shrine dedicated to Lord Shiva, located in Jammu and Kashmir. The cave temple is situated at an altitude of 3,888 meters and contains an ice stalagmite formed naturally, which is considered to be a Shiva Linga. The cave is accessible only for a short period during summer months.",
        "location": {
            "address": "Anantnag district, Jammu and Kashmir, India",
            "description": "Located in a cave in the Himalayas, accessible via Pahalgam or Baltal."
        },
        "nearby_attractions": [
            "Sheshnag Lake",
            "Pahalgam",
            "Chandanwari",
            "Baltal Valley",
            "Sonamarg"
        ],
        "transportation": {
            "air": "Nearest airport is Sheikh ul-Alam International Airport, Srinagar (102 km from Pahalgam)",
            "train": "Nearest railway station is Jammu Tawi (250 km away)",
            "bus": "Regular bus services from Srinagar to Pahalgam/Baltal",
            "local": "Helicopter services available during yatra season"
        },
        "accommodations": [
            {
                "name": "SASB Camps",
                "type": "Base Camps",
                "price_range": "Free or Nominal charges"
            },
            {
                "name": "Nunwan Base Camp",
                "type": "Tent Accommodation",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Baltal Base Camp",
                "type": "Tent Accommodation",
                "price_range": "Rs. 200-500 per night"
            }
        ]
    },
    {
        "name": "Venkateshwara Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "The Venkateshwara Temple, also known as Tirupati Balaji Temple, is located in Tirumala, Andhra Pradesh. It is one of the most visited religious sites in the world. The temple's origins are believed to date back to over 2,000 years, with inscriptions from various dynasties including the Cholas and Pallavas.",
        "location": {
            "address": "Tirumala, Tirupati, Andhra Pradesh 517504, India",
            "description": "Located on the seventh peak of Tirumala Hills in Andhra Pradesh."
        },
        "nearby_attractions": [
            "Akasa Ganga",
            "Papanasam Falls",
            "Sri Padmavathi Temple",
            "ISKCON Temple",
            "Silathoranam"
        ],
        "transportation": {
            "air": "Tirupati Airport (30 km away)",
            "train": "Tirupati Railway Station (25 km away)",
            "bus": "Regular bus services from all major cities in South India",
            "local": "TTD buses and prepaid taxis available"
        },
        "accommodations": [
            {
                "name": "TTD Guest Houses",
                "type": "Government Accommodation",
                "price_range": "Rs. 100-2,000 per night"
            },
            {
                "name": "Tirumala Cottages",
                "type": "Luxury Accommodation",
                "price_range": "Rs. 2,000-5,000 per night"
            },
            {
                "name": "Free Accommodation",
                "type": "Basic Dormitory",
                "price_range": "Free"
            }
        ]
    },
    {
        "name": "Kamakhya Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "The Kamakhya Temple is one of the oldest of the 51 Shakti Peethas, located in Guwahati, Assam. It is dedicated to the goddess Kamakhya and was rebuilt in 1565 by Koch king Naranarayana. The temple is an important center of Tantric practices and Shakti worship.",
        "location": {
            "address": "Nilachal Hill, Guwahati, Assam 781010, India",
            "description": "Located atop the Nilachal Hill in western Guwahati, Assam."
        },
        "nearby_attractions": [
            "Umananda Temple",
            "Navagraha Temple",
            "Brahmaputra River",
            "Assam State Museum",
            "Srimanta Sankardeva Kalakshetra"
        ],
        "transportation": {
            "air": "Lokpriya Gopinath Bordoloi International Airport, Guwahati (20 km away)",
            "train": "Guwahati Railway Station (7 km away)",
            "bus": "ISBT Guwahati with connections to all major cities",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "Kamakhya Temple Guest House",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Brahmaputra Ashok",
                "type": "Luxury Hotel",
                "price_range": "Rs. 3,000-6,000 per night"
            },
            {
                "name": "Nilachal Dormitory",
                "type": "Budget Accommodation",
                "price_range": "Rs. 500-1,000 per night"
            }
        ]
    },
    {
        "name": "Mallikarjuna Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "The Mallikarjuna Temple at Srisailam is one of the twelve Jyotirlinga temples dedicated to Lord Shiva. Located on the banks of Krishna River in Andhra Pradesh, the temple's architecture reflects various styles from the 7th century onwards. It is also one of the 51 Shakti Peethas.",
        "location": {
            "address": "Srisailam, Andhra Pradesh 528101, India",
            "description": "Located on Nallamala Hills, on the banks of Krishna River in Andhra Pradesh."
        },
        "nearby_attractions": [
            "Srisailam Dam",
            "Akkamahadevi Caves",
            "Sakshi Ganapati Temple",
            "Srisailam Wildlife Sanctuary",
            "Pathala Ganga"
        ],
        "transportation": {
            "air": "Nearest airport is Hyderabad International Airport (220 km away)",
            "train": "Nearest major railway station is Markapur (85 km away)",
            "bus": "Regular bus services from major cities in Andhra Pradesh and Telangana",
            "local": "Local buses and taxis available"
        },
        "accommodations": [
            {
                "name": "APTDC Hotel Haritha",
                "type": "Government Hotel",
                "price_range": "Rs. 1,000-2,500 per night"
            },
            {
                "name": "Srisailam Temple Cottages",
                "type": "Temple Accommodation",
                "price_range": "Rs. 500-1,500 per night"
            },
            {
                "name": "Hotel Mallikarjuna",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,800 per night"
            }
        ]
    },
    {
        "name": "Omkareshwar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Omkareshwar Temple is one of the twelve Jyotirlinga shrines, located on an island called Mandhata or Shivapuri in the Narmada river. The shape of the island is said to resemble the Hindu ॐ symbol. The temple's architecture dates back to the Medieval period.",
        "location": {
            "address": "Omkareshwar, Madhya Pradesh 450556, India",
            "description": "Located on an island in the Narmada River in Madhya Pradesh."
        },
        "nearby_attractions": [
            "Mamleshwar Temple",
            "Siddhnath Temple",
            "Kedareshwar Temple",
            "Narmada River Ghats",
            "Gauri Somnath Temple"
        ],
        "transportation": {
            "air": "Nearest airport is Devi Ahilyabai Holkar Airport, Indore (77 km away)",
            "train": "Nearest railway station is Omkareshwar Road (12 km away)",
            "bus": "Regular bus services from Indore and other major cities",
            "local": "Auto-rickshaws and boats available"
        },
        "accommodations": [
            {
                "name": "MP Tourism Hotel",
                "type": "Government Hotel",
                "price_range": "Rs. 800-2,000 per night"
            },
            {
                "name": "Narmada Resort",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Jyotirlinga Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            }
        ]
    },
    {
        "name": "Bhimashankar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Bhimashankar Temple is one of the twelve Jyotirlinga temples, located in Maharashtra. The temple is situated in the Bhimashankar Wildlife Sanctuary and is surrounded by ancient forests. The temple's Nagara style of architecture dates back to the 13th century.",
        "location": {
            "address": "Bhimashankar, Maharashtra 410509, India",
            "description": "Located in the Sahyadri range of the Western Ghats in Maharashtra."
        },
        "nearby_attractions": [
            "Bhimashankar Wildlife Sanctuary",
            "Hanuman Lake",
            "Gupt Bhimashankar",
            "Bombay Point",
            "Nagphani Point"
        ],
        "transportation": {
            "air": "Nearest airport is Pune International Airport (110 km away)",
            "train": "Nearest railway station is Pune Junction (120 km away)",
            "bus": "Regular bus services from Pune and Mumbai",
            "local": "Shared jeeps and taxis available"
        },
        "accommodations": [
            {
                "name": "MTDC Resort Bhimashankar",
                "type": "Government Resort",
                "price_range": "Rs. 1,000-2,500 per night"
            },
            {
                "name": "Temple Trust Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Mountain View",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            }
        ]
    },
    {
        "name": "Trimbakeshwar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Trimbakeshwar Temple is one of the twelve Jyotirlinga temples, located near Nashik, Maharashtra. The temple was built by Peshwa Balaji Baji Rao in the 18th century. It is unique as its Jyotirlinga has three faces embodying Lord Brahma, Lord Vishnu, and Lord Shiva.",
        "location": {
            "address": "Trimbak, Maharashtra 422212, India",
            "description": "Located at the source of the Godavari River in Maharashtra."
        },
        "nearby_attractions": [
            "Brahmagiri Hill",
            "Kushavarta Kund",
            "Gangadwar",
            "Neel Parvat",
            "Godavari Source Point"
        ],
        "transportation": {
            "air": "Nearest airport is Nashik Airport (40 km away)",
            "train": "Nearest railway station is Nashik Road (28 km away)",
            "bus": "Regular bus services from Nashik and Mumbai",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "MTDC Resort Trimbakeshwar",
                "type": "Government Resort",
                "price_range": "Rs. 1,000-2,500 per night"
            },
            {
                "name": "Trimbakeshwar Devasthan Trust",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Ganga Godavari",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            }
        ]
    },
    {
        "name": "Baidyanath Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Baidyanath Temple, also known as Baba Baidyanath Dham, is one of the twelve Jyotirlinga temples, located in Deoghar, Jharkhand. The temple complex consists of 22 temples and is one of the most sacred sites for devotees of Lord Shiva.",
        "location": {
            "address": "Deoghar, Jharkhand 814112, India",
            "description": "Located in the Santhal Parganas division of Jharkhand."
        },
        "nearby_attractions": [
            "Nandan Pahar",
            "Trikut Pahar",
            "Tapovan",
            "Satsang Ashram",
            "Rikhia Yoga Ashram"
        ],
        "transportation": {
            "air": "Nearest airport is Deoghar Airport (12 km away)",
            "train": "Baidyanath Dham Railway Station (1 km away)",
            "bus": "Regular bus services from major cities in Jharkhand and Bihar",
            "local": "Auto-rickshaws and cycle rickshaws available"
        },
        "accommodations": [
            {
                "name": "Baidyanath Temple Trust Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Hotel Baidyanath Vilas",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,000-2,500 per night"
            },
            {
                "name": "JTDC Tourist Complex",
                "type": "Government Accommodation",
                "price_range": "Rs. 800-2,000 per night"
            }
        ]
    },
    {
        "name": "Nageshwar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Nageshwar Temple is one of the twelve Jyotirlinga temples, located near Dwarka, Gujarat. The temple enshrines a Jyotirlinga of Lord Shiva and is believed to be the first among the Jyotirlingas. The current temple structure was built in the early 20th century.",
        "location": {
            "address": "Nageshwar Temple, Dwarka, Gujarat 361335, India",
            "description": "Located between Gomati Dwarka and Bet Dwarka in Gujarat."
        },
        "nearby_attractions": [
            "Dwarkadheesh Temple",
            "Bet Dwarka",
            "Rukmini Temple",
            "Gomati Ghat",
            "Lighthouse Beach"
        ],
        "transportation": {
            "air": "Nearest airport is Jamnagar Airport (137 km away)",
            "train": "Dwarka Railway Station (12 km away)",
            "bus": "Regular bus services from major cities in Gujarat",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "Gujarat Tourism Hotel",
                "type": "Government Hotel",
                "price_range": "Rs. 1,000-2,500 per night"
            },
            {
                "name": "Nageshwar Temple Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Dwarka Residency",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            }
        ]
    },
    {
        "name": "Grishneshwar Temple",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Grishneshwar Temple is one of the twelve Jyotirlinga temples, located near Ellora Caves in Maharashtra. The present temple was built by Ahilyabai Holkar in the 18th century. It is the smallest of the twelve Jyotirlinga temples but showcases exquisite architectural craftsmanship.",
        "location": {
            "address": "Ellora, Aurangabad, Maharashtra 431102, India",
            "description": "Located near the famous Ellora Caves in Maharashtra."
        },
        "nearby_attractions": [
            "Ellora Caves",
            "Daulatabad Fort",
            "Bibi Ka Maqbara",
            "Aurangabad Caves",
            "Panchakki"
        ],
        "transportation": {
            "air": "Nearest airport is Aurangabad Airport (30 km away)",
            "train": "Aurangabad Railway Station (30 km away)",
            "bus": "Regular bus services from major cities in Maharashtra",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "MTDC Resort Ellora",
                "type": "Government Resort",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Grishneshwar Temple Trust",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Kailas",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            }
        ]
    },
    {
        "name": "Shree Khatu Shyam Mandir",
        "type": "temple",
        "religion": "Hinduism",
        "history": "Shree Khatu Shyam Temple is dedicated to Khatu Shyam, who is believed to be an incarnation of Lord Krishna. Located in Rajasthan, the temple was built in the early 20th century. It is famous for its marble architecture and intricate carvings.",
        "location": {
            "address": "Khatu, Sikar, Rajasthan 332307, India",
            "description": "Located in the Sikar district of Rajasthan."
        },
        "nearby_attractions": [
            "Shyam Kund",
            "Shyam Bagicha",
            "Samadhi Sthal",
            "Old Khatu Temple",
            "Shyam Baba Museum"
        ],
        "transportation": {
            "air": "Nearest airport is Jaipur International Airport (110 km away)",
            "train": "Nearest railway station is Ringas Junction (25 km away)",
            "bus": "Regular bus services from major cities in Rajasthan",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "Khatu Shyam Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Hotel Shyam Palace",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,000-2,000 per night"
            },
            {
                "name": "Baba ki Haveli",
                "type": "Guest House",
                "price_range": "Rs. 500-1,000 per night"
            }
        ]
    },
    {
        "name": "Basilica of Bom Jesus",
        "type": "church",
        "religion": "Christianity",
        "history": "The Basilica of Bom Jesus, located in Goa, India, is a UNESCO World Heritage Site built in the 16th century. It holds the mortal remains of St. Francis Xavier, the renowned missionary of Portuguese India. The church is a remarkable example of Baroque architecture and is known for its elaborate gilded altars and intricate woodwork. It is one of the oldest churches in India and continues to be a significant pilgrimage site for Christians from around the world.",
        "location": {
            "address": "Old Goa Rd, Bainguinim, Goa 403402, India",
            "description": "Located in Old Goa, approximately 10 km from Panaji, the capital of Goa."
        },
        "nearby_attractions": [
            "Se Cathedral",
            "Church of St. Francis of Assisi",
            "Chapel of St. Catherine",
            "Archaeological Museum",
            "Church of St. Cajetan"
        ],
        "transportation": {
            "air": "Nearest airport is Goa International Airport, Dabolim (25 km away)",
            "train": "Nearest railway station is Karmali Railway Station (8 km away)",
            "bus": "Regular bus services from major cities in Goa",
            "local": "Taxis and auto-rickshaws available"
        },
        "accommodations": [
            {
                "name": "Hospedaria Venite",
                "type": "Budget Hotel",
                "price_range": "Rs. 1,000-2,000 per night"
            },
            {
                "name": "Vivanta Goa, Panaji",
                "type": "Luxury Hotel",
                "price_range": "Rs. 5,000-10,000 per night"
            },
            {
                "name": "Old Goa Residency",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 2,000-4,000 per night"
            }
        ]
    },
    {
        "name": "Palitana Jain Temples",
        "type": "temple",
        "religion": "Jainism",
        "history": "The Palitana Jain Temples, located on Shatrunjaya Hill in Gujarat, comprise over 900 temples built over a period of 900 years, starting from the 11th century. These marble temples are considered the most sacred pilgrimage site for Shvetambara Jains. The main temple is dedicated to Adinath, the first Jain Tirthankara. Devotees need to climb 3,500 steps to reach the temple complex at the summit.",
        "location": {
            "address": "Shatrunjaya Hill, Palitana, Gujarat 364270, India",
            "description": "Located on Shatrunjaya Hill, near Palitana town in Gujarat."
        },
        "nearby_attractions": [
            "Hastagiri Jain Temple",
            "Talaja Caves",
            "Gopnath Beach",
            "Lothal",
            "Kundeshwar"
        ],
        "transportation": {
            "air": "Nearest airport is Rajkot Airport (160 km away)",
            "train": "Nearest railway station is Palitana Railway Station (4 km away)",
            "bus": "Regular bus services from major cities in Gujarat",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "GTDC Hotel Toran",
                "type": "Government Hotel",
                "price_range": "Rs. 800-1,500 per night"
            },
            {
                "name": "Vijay Vilas Palace Heritage Hotel",
                "type": "Heritage Hotel",
                "price_range": "Rs. 3,000-6,000 per night"
            },
            {
                "name": "Jain Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            }
        ]
    },
    {
        "name": "Shri Sammed Shikharji",
        "type": "temple",
        "religion": "Jainism",
        "history": "Shri Sammed Shikharji, also known as Parasnath Hill, is located in Jharkhand and is the most sacred pilgrimage site for Jains. It is believed that 20 out of the 24 Jain Tirthankaras attained moksha (salvation) here. The site consists of multiple temples and shrines spread across the Parasnath Hill. Pilgrims need to walk approximately 27 km uphill to visit all the tonks (shrines) on the summit.",
        "location": {
            "address": "Parasnath Hill, Madhuban, Jharkhand 825329, India",
            "description": "Located on Parasnath Hill in the Giridih district of Jharkhand."
        },
        "nearby_attractions": [
            "Madhuban",
            "Jain Temple in Madhuban",
            "Usri Falls",
            "Parasnath Railway Station",
            "Giridih Town"
        ],
        "transportation": {
            "air": "Nearest airport is Ranchi Airport (170 km away)",
            "train": "Nearest railway station is Parasnath Station (25 km away)",
            "bus": "Regular bus services from Dhanbad and Giridih",
            "local": "Jeeps and taxis available to reach the base of the hill"
        },
        "accommodations": [
            {
                "name": "Digambar Jain Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Shwetambar Jain Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 200-500 per night"
            },
            {
                "name": "Hotel Shalini",
                "type": "Budget Hotel",
                "price_range": "Rs. 800-1,500 per night"
            }
        ]
    },
    {
        "name": "Ranakpur Jain Temple",
        "type": "temple",
        "religion": "Jainism",
        "history": "The Ranakpur Jain Temple, built in the 15th century, is dedicated to Adinatha and is known for its architectural grandeur. Located in the Pali district of Rajasthan, it is constructed of light-colored marble and features 1,444 uniquely carved pillars. The temple was built under the patronage of the Rajput ruler Rana Kumbha, and its design is attributed to the architect Dharna Shah.",
        "location": {
            "address": "Ranakpur, Pali District, Rajasthan 306702, India",
            "description": "Located in a valley of the Aravalli Range, midway between Udaipur and Jodhpur in Rajasthan."
        },
        "nearby_attractions": [
            "Kumbhalgarh Fort",
            "Surya Narayan Temple",
            "Muchhal Mahavir Temple",
            "Sadri Town",
            "Ghanerao Castle"
        ],
        "transportation": {
            "air": "Nearest airport is Udaipur Airport (90 km away)",
            "train": "Nearest railway station is Falna Railway Station (30 km away)",
            "bus": "Regular bus services from Udaipur and Jodhpur",
            "local": "Taxis and jeeps available"
        },
        "accommodations": [
            {
                "name": "Maharani Bagh Orchard Retreat",
                "type": "Heritage Hotel",
                "price_range": "Rs. 5,000-8,000 per night"
            },
            {
                "name": "Ranakpur Hill Resort",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 2,000-4,000 per night"
            },
            {
                "name": "Jain Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            }
        ]
    },
    {
        "name": "Dilwara Temples",
        "type": "temple",
        "religion": "Jainism",
        "history": "The Dilwara Temples, located in Mount Abu, Rajasthan, are renowned for their extraordinary marble carvings and architectural perfection. Built between the 11th and 13th centuries AD by Chalukya dynasty, they are among the most exquisite examples of Jain temple architecture. The five temples are dedicated to different Jain Tirthankaras and are a testament to the skill of the artisans of that era.",
        "location": {
            "address": "Mount Abu, Rajasthan 307501, India",
            "description": "Located in Mount Abu, the only hill station in Rajasthan, at an altitude of 1,220 meters above sea level."
        },
        "nearby_attractions": [
            "Nakki Lake",
            "Guru Shikhar",
            "Achalgarh Fort",
            "Sunset Point",
            "Mount Abu Wildlife Sanctuary"
        ],
        "transportation": {
            "air": "Nearest airport is Udaipur Airport (185 km away)",
            "train": "Nearest railway station is Abu Road Railway Station (25 km away)",
            "bus": "Regular bus services from major cities in Rajasthan and Gujarat",
            "local": "Taxis and auto-rickshaws available"
        },
        "accommodations": [
            {
                "name": "Palace Hotel",
                "type": "Heritage Hotel",
                "price_range": "Rs. 4,000-8,000 per night"
            },
            {
                "name": "Jain Dharamshala",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Hillock",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 2,000-4,000 per night"
            }
        ]
    },
    {
        "name": "Kulpakji Jain Temple",
        "type": "temple",
        "religion": "Jainism",
        "history": "Kulpakji Temple, also known as Kolanupaka Temple, is a 2,000-year-old Jain temple located in Telangana. It houses an idol of Lord Rishabhanatha made of monolithic black stone and is one of the oldest and most sacred Jain pilgrimage sites in South India. The temple underwent renovation in the 12th century under the Kalyani Chalukyas. It is known for its beautiful architecture and intricate stone carvings.",
        "location": {
            "address": "Kolanupaka, Aler Mandal, Yadadri Bhuvanagiri District, Telangana 508126, India",
            "description": "Located in Kolanupaka village, about 80 km from Hyderabad, Telangana."
        },
        "nearby_attractions": [
            "Kolanupaka Archaeological Museum",
            "Someshwara Temple",
            "Yadadri Temple",
            "Aler Fort",
            "Bhongir Fort"
        ],
        "transportation": {
            "air": "Nearest airport is Hyderabad International Airport (80 km away)",
            "train": "Nearest railway station is Aler Railway Station (10 km away)",
            "bus": "Regular bus services from Hyderabad and other towns in Telangana",
            "local": "Auto-rickshaws and taxis available"
        },
        "accommodations": [
            {
                "name": "Jain Dharamshala Kolanupaka",
                "type": "Dharamshala",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Bhongir Fort Resort",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Hyderabad Hotels",
                "type": "Various Options",
                "price_range": "Rs. 1,000-10,000 per night"
            }
        ]
    },
    {
        "name": "Khwaja Gharib Nawaz Dargah Sharif",
        "type": "dargah",
        "religion": "Islam",
        "history": "The Dargah of Khwaja Moinuddin Chishti, also known as Khwaja Gharib Nawaz Dargah Sharif, is located in Ajmer, Rajasthan. It is the final resting place of Khwaja Moinuddin Chishti, a Sufi saint who arrived in India in 1192 CE. The Dargah was built in the 13th century and has been visited by emperors, kings, and people from all religions seeking blessings. It is particularly famous for its Urs festival which commemorates the death anniversary of the saint.",
        "location": {
            "address": "Dargah Sharif, Ajmer, Rajasthan 305001, India",
            "description": "Located in the heart of Ajmer city in Rajasthan."
        },
        "nearby_attractions": [
            "Ana Sagar Lake",
            "Taragarh Fort",
            "Adhai Din Ka Jhonpra",
            "Mayo College",
            "Pushkar Lake (16 km away)"
        ],
        "transportation": {
            "air": "Nearest airport is Jaipur International Airport (130 km away)",
            "train": "Ajmer Junction Railway Station (2 km away)",
            "bus": "Regular bus services from major cities in Rajasthan",
            "local": "Auto-rickshaws and cycle-rickshaws available"
        },
        "accommodations": [
            {
                "name": "Hotel Ajmer Inn",
                "type": "Mid-range Hotel",
                "price_range": "Rs. 1,500-3,000 per night"
            },
            {
                "name": "Dargah Sharif Guest House",
                "type": "Budget Accommodation",
                "price_range": "Rs. 300-800 per night"
            },
            {
                "name": "Hotel Embassy",
                "type": "Luxury Hotel",
                "price_range": "Rs. 3,000-6,000 per night"
            }
        ]
    }
]

# Insert sample data into the collection
places_collection.insert_many(sample_places)

print(f"Successfully inserted {len(sample_places)} sample places into the database.")
print("Database initialization complete!") 