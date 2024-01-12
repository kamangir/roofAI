def generate_seed() -> str:
    list_of_modules = [
        "init",
        "log",
        "project",
        "layer",
        "application",
        "seed",
        "QGIS",
        "apps/vanwatch",
        "main",
    ]

    seed = "; ".join(
        [
            'exec(Path(f\'{os.getenv("HOME")}/git/roofAI/roofAI/QGIS/console/'
            + module_name
            + ".py').read_text())"
            for module_name in list_of_modules
        ]
    )

    return seed
