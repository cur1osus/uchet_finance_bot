from rapidfuzz import fuzz, utils, process

print(
    process.extract(
        query="дюшес reboot",
        choices=["[М+]ЧЕРНОГОЛ.Нап.ДЮШЕС б/а с/г 1л", "дюшес"],
        scorer=fuzz.WRatio,
        limit=5,
        processor=utils.default_process,
    )
)
