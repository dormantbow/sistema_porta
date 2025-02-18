import smtplib
from email.mime.text import MIMEText

def send_error_report(user_email, error_description):
    """Envia um e-mail com a descrição do erro."""
    
    # Configurações do e-mail
    sender_email = "melquessedequipedro@gmail.com"  # Seu e-mail
    sender_password = "ogfi trki qehz vnub"  # Sua senha do gmail
    recipient_email = "melquessedequipedro@gmail.com"  # E-mail de suporte
    
    subject = "Novo Relato de Erro no Sistema de Portas"
    message = f"Usuário: {user_email}\n\nErro Reportado:\n{error_description}"

    # Criar o e-mail
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        # Conectar ao servidor SMTP e enviar o e-mail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Segurança
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True  # Sucesso
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False  # Falha
