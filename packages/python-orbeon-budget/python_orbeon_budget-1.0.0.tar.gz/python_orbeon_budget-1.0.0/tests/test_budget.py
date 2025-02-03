import unittest

from io import BytesIO
from pathlib import Path
from python_orbeon_budget.budget import Budget


BASE_DIR = Path(__file__).resolve().parent.parent

def logo_path():
    BASE_DIR = Path(__file__).resolve().parent
    return BASE_DIR / 'orbeon_stamped' / 'contents' / 'logo.png'

def watermark_path():
    BASE_DIR = Path(__file__).resolve().parent
    return BASE_DIR / 'orbeon_stamped' / 'contents' / 'watermark.png'

def get_bytesio(path):
    with open(path, 'rb') as f:
        return BytesIO(f.read())

def get_context():
    context = {
        'logo': logo_path(),
        'watermark': watermark_path,
        'id': '30.381',
        'generated_in': {
            'text': 'Orçamento gerado em:',
            'value': '01/02/2025 às 15:30'
        },
        'seller': {
            'text': 'Vendedor | Telefone/WhatsApp:',
            'value': 'Eduardo Rabelo | (31) 3207-0000'
        },
        'valid': {
            'text': 'Válido por:',
            'value': '7 dias úteis'
        },
        'production_time': {
            'text': 'Prazo de produção:',
            'value': '5 dias úteis'
        },
        "products": [
            {"name": "Teclado Mecânico", "quantity": "2,0000", "unit_price": "R$ 250,00", "subtotal": "R$ 500,00"},
            {"name": "Mouse Gamer", "quantity": "1,0000", "unit_price": "R$ 180,50", "subtotal": "R$ 180,50"},
            {"name": "Monitor 24''", "quantity": "3,0000", "unit_price": "R$ 1200,00", "subtotal": "R$ 3.600,00"},
            {"name": "Headset Bluetooth", "quantity": "1,0000", "unit_price": "R$ 350,00", "subtotal": "R$ 350,00"},
            {"name": "Cadeira Gamer", "quantity": "1,0000", "unit_price": "R$ 1500,00", "subtotal": "R$ 1500,00"},
            {"name": "Mousepad RGB", "quantity": "2,0000", "unit_price": "R$ 120,00", "subtotal": "R$ 240,00"},
        ],
        "condition": {
            "title": "Condições",
            "conditions": [
                "A data de entrega é válida desde que o prazo para upload seja respeitado e o pagamento esteja aprovado.",
                "O valor total corresponde à soma dos preços dos produtos. Para itens com múltiplas quantidades, todos os valores são somados.",
                "Os valores estão sujeitos a alterações sem aviso prévio.",
                "Este orçamento tem validade de 72 horas."
            ],
        },
        'footer': {
            'r1': "Scápole Camisetas Personalizadas - scapole.com",
            'r2': "Contato: (31) 3207-0000 | contato@scapole.com"
        },
    }
    return context


class TestBudget(unittest.TestCase):

    def test_gen(self):
        context = get_context()
        file_save_path = "generated_files_saved/orcamento.pdf"
        budget = Budget(file_save_path, context)
        budget.draw()
        for i in range(1, 4): budget.new_page()
        budget.save()
        empty = True
        if file_save_path.exists():
            if file_save_path.stat().st_size > 500:
                empty = False
        self.assertFalse(empty)

if __name__ == "__main__":
    unittest.main()
