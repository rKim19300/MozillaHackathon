#!/usr/bin/env python3
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",  # Run your llamafile first, this is the port that it's running on
    api_key="sk-no-key-required"
)

sampleText = """Meta builds technologies and services that enable people to connect with each other, build communities, and grow businesses. These Terms of Service (the "Terms") govern your access and use of Facebook, Messenger, and the other products, websites, features, apps, services, technologies, and software we offer (the Meta Products or Products), except where we expressly state that separate terms (and not these) apply. (For example, your use of Instagram is subject to the Instagram Terms of Use). These Products are provided to you by Meta Platforms, Inc. These Terms therefore constitute an agreement between you and Meta Platforms, Inc. If you do not agree to these Terms, then do not access or use Facebook or the other products and services covered by these Terms.

These Terms (formerly known as the Statement of Rights and Responsibilities) make up the entire agreement between you and Meta Platforms, Inc. regarding your use of our Products. They supersede any prior agreements.

We don’t charge you to use Facebook or the other products and services covered by these Terms, unless we state otherwise. Instead, businesses and organizations, and other persons pay us to show you ads for their products and services. By using our Products, you agree that we can show you ads that we think may be relevant to you and your interests. We use your personal data to help determine which personalized ads to show you.

We don’t sell your personal data to advertisers, and we don’t share information that directly identifies you (such as your name, email address or other contact information) with advertisers unless you give us specific permission. Instead, advertisers can tell us things like the kind of audience they want to see their ads, and we show those ads to people who may be interested. We provide advertisers with reports about the performance of their ads that help them understand how people are interacting with their content. See Section 2 below to learn more about how personalized advertising under these terms works on the Meta Products.

Our Privacy Policy explains how we collect and use your personal data to determine some of the ads you see and provide all of the other services described below. You can also go to your settings pages of the relevant Meta Product at any time to review the privacy choices you have about how we use your data."""

prompt = f"""
    Please read the following privacy policy or terms of service and summarize the key points and concerns regarding the collection, use, and sharing of consumer data. Specifically, focus on:

    1. What types of data are being collected (e.g., personal information, browsing data, payment details, etc.).
    2. How the data is being used (e.g., for advertising, service improvement, sharing with third parties, etc.).
    3. Who the data is being shared with (e.g., third-party partners, advertisers, government authorities, etc.).
    4. How long the data is retained and under what conditions it is deleted or anonymized.
    5. Any rights or control given to consumers over their data (e.g., opt-out options, data access, correction, or deletion requests).
    6. Security measures in place to protect consumer data.
    7. Any potential risks or concerns related to data privacy or data sharing.

    Provide a concise bullet-point summary highlighting these key aspects.

    ----
    {sampleText}
    """

completion = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[
        {"role": "system",
         "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
        {"role": "user", "content": f"{prompt}"}
    ]
)

response = completion.choices[0].message

print(response.content)
