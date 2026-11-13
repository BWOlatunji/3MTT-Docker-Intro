# Docker demo 


Download the images

```bash
docker login
docker pull python:3.12-slim
docker pull postgres:16
docker pull adminer
```

---

## Slide 13: A Dockerfile is a recipe

```bash
cd sales-report
ls -a
cat Dockerfile
```
**What is in the Dockerfile**

- **FROM** starts from the official slim Python 3.12 image.
- **WORKDIR** means everything after this happens in `/app` inside the image.
- **COPY requirements.txt** copies the package list in first. Slide 14 explains why.
- **RUN pip install** runs once, at build time.
- **COPY . .** copies the rest of the project. `.dockerignore` keeps junk out.
- **CMD** runs every time a container starts.

Then build and run:

```bash
docker build -t sales-report:1.0 .
docker run --rm sales-report:1.0
```

Expected output:

```
            sales
count    3.000000
mean   131.666667
std     43.684475
min     95.000000
25%    107.500000
50%    120.000000
75%    150.000000
max    180.000000
```

The final `.` in `docker build`: it means "use this folder".

## Slide 14: Layers and caching

1. Open `app.py` in your editor and add one line at the end:

   ```python
   print("Total sales:", df["sales"].sum())
   ```

2. Rebuild with a new tag:

   ```bash
   docker build -t sales-report:1.1 .
   ```

3. The `RUN pip install` step shows **CACHED**. Only `COPY . .` and the steps after it re-run, so the rebuild finishes in seconds.

4. Run the new version:

   ```bash
   docker run --rm sales-report:1.1
   ```

   The last line now reads `Total sales: 395`.

5. Run `docker images` to show both tags, 1.0 and 1.1, side by side.

Optional contrast: add `numpy` to `requirements.txt` and rebuild. The pip step now re-runs, because its input changed.


## Slide 17: Docker Compose (about 3 min)

```bash
cd ~/Desktop/docker-demo-kit/compose-demo
cat compose.yaml
docker compose up -d
docker compose ps
```

Open http://localhost:8080 and log in to Adminer:

| Field    | Value      |
|----------|------------|
| System   | PostgreSQL |
| Server   | `db`       |
| Username | `postgres` |
| Password | `example`  |
| Database | leave blank |

Typing `db` as the server name shows that services find each other by service name.

Optional: in Adminer, click **SQL command** and run:

```sql
CREATE TABLE sales (product text, amount int);
INSERT INTO sales VALUES ('A', 120), ('B', 95), ('C', 180);
```

The data survives a restart:

```bash
docker compose down        # containers removed, volume kept
docker compose up -d       # log in again: the sales table is still there
```

Finially:

```bash
docker compose logs db     # show logs
docker compose down        # stop
```

## Reset after your session

```bash
cd ~/Desktop/docker-demo-kit/compose-demo && docker compose down -v
docker rmi sales-report:1.0 sales-report:1.1
```

