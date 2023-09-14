from datetime import datetime
from functions_async import main
import asyncio


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start)
