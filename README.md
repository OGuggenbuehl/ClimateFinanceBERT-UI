# ClimateFinanceBERT-UI

<div align="center">
  <img src="src/assets/tumthinktank-logo.svg" alt="TUM Think Tank Logo" width="120">
    <h3>Climate Finance Analysis & Visualization Platform</h3>
      <p>An interactive dashboard for exploring and analyzing global climate finance data powered by the <a href="https://github.com/MalteToetzke/consistent-and-replicable-estimation-of-bilateral-climate-finance">ClimateFinanceBERT</a> model as described in <a href="https://doi.org/10.1038/s41558-022-01482-7">Toetzke, M., Stünzi, A. & Egli, F. (2022)</a>.</p>
</div>

## 📊 Features

- **Interactive Map Visualization**: View global climate finance flows 
- **Data Analysis Tools**: Country statistics and detailed breakdowns by year range, categories, and flow types
- **Export Capabilities**: Download data as queried from the dashboard
- **User-Friendly Interface**: Built with Dash and Plotly for an intuitive user experience

## 🚀 Getting Started

### Prerequisites

- Python 3.12+ 
- [Make](https://www.gnu.org/software/make/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ClimateFinanceBERT-UI.git
cd ClimateFinanceBERT-UI
```

There is a host of convenient Make-commands to navigate the project. You can view all available commands by running:
```bash
make help
```

2. Install dependencies using the provided Makefile:
```bash
make install
```
   
This will:
- Install [uv](https://docs.astral.sh/uv/) package manager
- Create a [virtual environment](https://docs.python.org/3/library/venv.html)
- Install dependencies as defined in `pyproject.toml`
- Set up [direnv](https://direnv.net/) for environment management

3. Prepare the database:
```bash
make duckdb-pipeline
```

### Running the Application

Start the application locally:
```bash
make run
```

For development with automatic code formatting and linting:
```bash
make dev
```

The application will be available at [http://localhost:8050](http://localhost:8050).

### Using Docker

Several Docker commands are available:

```bash
# Build application image and run container in detached mode
make docker-up

# Stop detached container
make docker-down

# Build application image
make docker-build

# Build the application image in development mode
make docker-dev

# View logs
make docker-logs
```

You can customize the port by setting the PORT environment variable:
```bash
PORT=8051 make docker-up
```

## 🏗️ Project Structure

```
ClimateFinanceBERT-UI/
├── data/               # Data files
├── docker/             # Docker configuration
├── notebooks/          # Jupyter notebooks for exploration
└── src/                # Source code
    ├── app.py          # Application entry point
    ├── assets/         # CSS, fonts, and static assets
    ├── callbacks/      # Dash callback functions
    ├── components/     # UI components and widgets
    ├── pages/          # Application page layouts
    └── utils/          # Utility functions and helpers
```

## 📝 License

[MIT License](LICENSE)

## 👥 Contributors

- Oliver Guggenbühl

## 🙏 Acknowledgements

- The ClimateFinanceBERT model and research team
    - Anna Stünzi - Universität St. Gallen
    - Florian Egli - TUM Think Tank
    - Malte Toetzke - TUM Think Tank
- TUM Think Tank for supporting the project
