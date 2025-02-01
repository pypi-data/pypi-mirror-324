from setuptools import setup, find_packages

setup(
    name='CnEngineLinux',
    version='0.1.5',
    packages=find_packages(),  # Automaticky najde všechny balíčky v adresáři
    install_requires=[
        # Přidej další externí knihovny, pokud je třeba
        'pyopenssl',
    ],
    entry_points={
        'console_scripts': [
            'cnserver = cn_engine_linux.cnserver:main',
            'cnsearch = cn_engine_linux.cnsearch:main',
            'cnview = cn_engine_linux.cnview:main',
        ],
    },
    author='Rasmnout',
    author_email='rasmnout@gmail.com',
    description='CnEngine v0.1.5 is a lightweight console-based communication protocol with CN (basic), CNSS (secure SSL), and CNF (file delivery) protocols. It includes a custom language for creating structured console pages.',
    long_description='CnEngine v0.1.5 is a simple, console-based communication protocol similar to HTTP, designed for lightweight and efficient text-based interactions. It supports three main protocols: CN (basic and unencrypted), CNSS (secure SSL communication), and CNF (file-based content delivery). Additionally, it includes a custom programming language, CN, for creating structured console-based pages.',
    long_description_content_type='text/plain',
    url='https://rasmnout.github.io',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
