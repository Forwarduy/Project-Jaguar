git clone https://github.com/Forwarduy/Project-Jaguar.git
cd Project-Jaguar
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python main.py hello
