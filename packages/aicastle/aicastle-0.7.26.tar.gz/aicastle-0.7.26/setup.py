from setuptools import setup, find_packages
from get_version import read_version

setup(
    name='aicastle',
    version=read_version(),
    packages=find_packages(include=['aicastle', 'aicastle.*']),
    include_package_data=True,
    package_data={
        'aicastle': ['package_data/*'],
    },
    
    # 의존성
    install_requires=[ 
        'tqdm', 
        'ipykernel',
        # 'pandas', 
        # 'scikit-learn',
        "click",      # CLI 도구

        ## drfc-aws
        "boto3",
        "paramiko",
        # "python-dotenv",

        ### chat
        "pyyaml",
        "streamlit",  # Streamlit 의존성
        'openai',
        'tiktoken',
        'pathspec',
        'pymupdf',
        'python-dotenv',
        # 'python-magic',
        
        # 'azure-identity',
        # 'boto3',

        'pillow',

        ## deepracer
        'opencv-python',
        'tensorflow',
        'requests-toolbelt',
        'beautifulsoup4',
        'lxml',
        'pynput',
        'paramiko',
        'ollama',


    ],

    entry_points={
        "console_scripts": [
            "aicastle=aicastle.cli:main",  # aicastle 명령어 실행 엔트리포인트
        ],
    },

    author='aicastle',
    author_email='dev@aicastle.io',
    description='AI Castle Package',
    url='https://github.com/ai-castle/aicastle',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    zip_safe=False,
)
