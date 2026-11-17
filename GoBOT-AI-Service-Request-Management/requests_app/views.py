
from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GoBOT - AI Service Request Management</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
            }

            header {
                background: #172554;
                color: white;
                padding: 22px 8%;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            header h2 {
                font-size: 27px;
            }

            nav a {
                color: white;
                text-decoration: none;
                margin-left: 22px;
                font-size: 15px;
            }

            .hero {
                text-align: center;
                padding: 85px 20px;
                background: linear-gradient(135deg, #dbeafe, #eff6ff);
            }

            .hero h1 {
                font-size: 42px;
                color: #172554;
                margin-bottom: 20px;
            }

            .hero p {
                font-size: 18px;
                color: #475569;
                margin-bottom: 28px;
                line-height: 1.7;
            }

            .btn {
                display: inline-block;
                background: #2563eb;
                color: white;
                padding: 14px 28px;
                border-radius: 8px;
                text-decoration: none;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }

            .btn:hover {
                background: #1d4ed8;
            }

            .services {
                padding: 55px 8%;
                text-align: center;
            }

            .services h2 {
                font-size: 30px;
                margin-bottom: 35px;
                color: #172554;
            }

            .cards {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 25px;
            }

            .card {
                background: white;
                padding: 30px;
                width: 270px;
                border-radius: 12px;
                box-shadow: 0 4px 12px #00000012;
            }

            .card h3 {
                color: #2563eb;
                margin-bottom: 15px;
            }

            .card p {
                color: #64748b;
                line-height: 1.6;
            }

            footer {
                background: #172554;
                color: white;
                text-align: center;
                padding: 22px;
                margin-top: 40px;
            }

            @media(max-width: 600px) {
                header {
                    flex-direction: column;
                    gap: 15px;
                }

                nav a {
                    margin: 7px;
                }

                .hero h1 {
                    font-size: 30px;
                }
            }
        </style>
    </head>

    <body>

        <header>
            <h2>GoBOT</h2>

            <nav>
                <a href="/">Home</a>
                <a href="#services">Services</a>
                <a href="#about">About</a>
            </nav>
        </header>

        <section class="hero">
            <h1>Welcome to GoBOT!</h1>

            <p>
                AI-Powered Service Request Management System
                <br>
                Manage your service requests easily, quickly and smartly.
            </p>

            <button class="btn" onclick="showMessage()">
                Get Started
            </button>
        </section>

        <section class="services" id="services">
            <h2>Our Features</h2>

            <div class="cards">

                <div class="card">
                    <h3>Submit Request</h3>
                    <p>
                        Submit your service requests
                        easily through our platform.
                    </p>
                </div>

                <div class="card">
                    <h3>Track Requests</h3>
                    <p>
                        Check the status of your
                        submitted service requests.
                    </p>
                </div>

                <div class="card">
                    <h3>AI Assistance</h3>
                    <p>
                        Get smart assistance for
                        your service-related questions.
                    </p>
                </div>

            </div>
        </section>

        <section class="services" id="about">
            <h2>About GoBOT</h2>

            <p>
                GoBOT is an AI-based service request
                management platform designed to make
                request handling simple and efficient.
            </p>
        </section>

        <footer>
            <p>© 2026 GoBOT - AI Service Request Management System</p>
        </footer>

        <script>
            function showMessage() {
                alert("Welcome to GoBOT! Your smart service platform.");
            }
        </script>

    </body>
    </html>
    """

    return HttpResponse(html)
