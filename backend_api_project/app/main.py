# main.py
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
# from app.auth import login, register, forget_password, reset_password
# from app.files import upload

from auth import login, register, forget_password, reset_password , get_users
from files import upload


import laspy
import numpy as np

app = FastAPI()


# MongoDB settings
MONGO_DB_URL = "mongodb://mongo:27017"
MONGO_DB_NAME = "test_db"

# MongoDB connection
client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[MONGO_DB_NAME]


# Include authentication routes
app.include_router(login.router)
app.include_router(register.router)
app.include_router(forget_password.router)
app.include_router(reset_password.router)

# Include auth users route
app.include_router(get_users.router)


# Include file upload route
app.include_router(upload.router)

# @app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def read_root():
    return {"message": "Hello, Wo asrld!"}

@app.get("/users")
async def read_users():
    mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = mongo_client["auth_db"]
     
    # mongo_client = AsyncIOMotorClient("mongodb://localhost:27017")
    # db = mongo_client["auth_db"]
    # users_collection = db["users"]
    # print("Users")
    # print(db)
    # users_collection = db["users"]
    # print(users_collection)
    # users = []
    # async for user in users_collection.find():
    #     users.append(user)
    # return users

    try:
        users_collection = db["users"]
        users = []
        async for user in users_collection.find():
            users.append(user)
        return users
    except Exception as e:
        return {"error": str(e)}
    




@app.get("/cal")
async def read_cal():
    files_collection = db["files"]
    file = files_collection.find_one()


    las_file_path = file
    # read .las
    # las_file_path
    # las_file_path = "../app/data/uploads/Left_Rocks21.las"
    # app/data/uploads/Left_Rocks21.las
    data_prepare = []

    with laspy.open(las_file_path) as las:
        file = las.read()
        z_coords = np.array(file.z)
        x_coords = np.array(file.x)
        y_coords = np.array(file.y)

        for data in range(len(file)):
            data_prepare.append([x_coords[data], y_coords[data], z_coords[data]])
            if data == 1000:
                break

    # print(data_prepare)
    print(f"{las_file_path.split('/').pop()} have point = {len(data_prepare)}")

    display_data = data_prepare[:10]
    # list: [x, y, z]
    # data_prepare = [[x, y, z], [x, y, z], ...]
    # return data_prepare

    return {
        "message": "Hello, World!",
        "data": display_data,
        }


@app.get("/volume")
async def read_den():

    files_collection = db["files"]
    file = files_collection.find_one()


    inFile = file

    # inFile = laspy.read("../app/data/uploads/23_sand.las")

    # Extract X, Y, and Z coordinates from the LAS file
    x_coords = inFile.x
    y_coords = inFile.y
    z_coords = inFile.z

    # Define the base level (minimum Z value)
    base_level = np.min(z_coords)


    # Define the size of each grid cell
    grid_size = 1  # Adjust this according to your requirement

    # Create a grid
    x_range = np.arange(np.min(x_coords), np.max(x_coords), grid_size)
    y_range = np.arange(np.min(y_coords), np.max(y_coords), grid_size)

    # Initialize total volume
    total_volume = 0

    # Loop through each grid cell
    for x in x_range:
        for y in y_range:
            # Filter points in the current cell
            cell_points = inFile.points[((x_coords >= x) & (x_coords < x + grid_size) &
                                    (y_coords >= y) & (y_coords < y + grid_size))]
            num_points_in_cell = len(cell_points)
            # Calculate the volume contribution for each point within the cell
            for point in cell_points:
                point_volume = max(0, (point['Z'] - base_level) * (grid_size * 5)**2)  # Ensure non-negative volume
                normalized_point_volume = point_volume / num_points_in_cell
                total_volume += normalized_point_volume
    
    return {
        "message": "Hello, World!",
        "data": f"Total Volume: {total_volume:,.0f} cm³",
    }






    # # read .las
    # # las_file_path
    # las_file_path = "../app/data/uploads/Left_Rocks21.las"
    # # app/data/uploads/Left_Rocks21.las
    # data_prepare = []

    # with laspy.open(las_file_path) as las:
    #     file = las.read()
    #     z_coords = np.array(file.z)
    #     x_coords = np.array(file.x)
    #     y_coords = np.array(file.y)

    #     for data in range(len(file)):
    #         data_prepare.append([x_coords[data], y_coords[data], z_coords[data]])
    #         if data == 1000:
    #             break

    # # print(data_prepare)
    # print(f"{las_file_path.split('/').pop()} have point = {len(data_prepare)}")

    # display_data = data_prepare[:10]
    # # list: [x, y, z]
    # # data_prepare = [[x, y, z], [x, y, z], ...]
    # # return data_prepare

    

    # return {
    #     "message": "Hello, World!",
    #     "data": "display_data",
    #     }


@app.get("/add/noise")
async def read_add_noise(body):

    noise = body["noise"]

    files_collection = db["files"]
    file = files_collection.find_one()


    inFile = file
    # inFile = laspy.read("../app/data/uploads/23_sand.las")

    # Extract x, y, z coordinates
    x = inFile.x
    y = inFile.y
    z = inFile.z

    # Extract RGB color channels
    red = inFile.red
    green = inFile.green
    blue = inFile.blue

    # Normalize color values to [0, 1]
    # red_normalized = red / 65535.0
    # green_normalized = green / 65535.0
    # blue_normalized = blue / 65535.0

    # Add Gaussian noise to x, y, z coordinates
    mu, sigma = 0, 0.01  # mean and standard deviation
    noise_x = np.random.normal(mu, sigma, len(x))
    noise_y = np.random.normal(mu, sigma, len(y))
    noise_z = np.random.normal(mu, sigma, len(z))

    x_noisy = x + noise_x
    y_noisy = y + noise_y
    z_noisy = z + noise_z

    return {
        "message": "Hello, World!",
        "data": {
            "x_noisy": x_noisy,
            "y_noisy": y_noisy,
            "z_noisy": z_noisy,
            "x_original": x,
            "y_original": y,
            "z_original": z,
        },
    }


@app.get("/remove/noise")
async def read_remove_noise(body):

    noise = body["noise"]
    
    files_collection = db["files"]
    file = files_collection.find_one()


    inFile = file
    #Open the LAS file for reading
    # inFile = laspy.read("../app/data/uploads/23_sand.las")

    #Define grid parameters (you can adjust these)
    grid_size_x = 5  # Grid cell size along X-axis
    grid_size_y = 5 # Grid cell size along Y-axis

    #Calculate grid indices for each point
    grid_x = np.floor(inFile.x / grid_size_x)
    grid_y = np.floor(inFile.y / grid_size_y)

    #Create a dictionary to store points in each grid cell
    grid_points = {}

    for i in range(len(inFile.points)):
        x, y = inFile.x[i], inFile.y[i]
        grid_index = (grid_x[i], grid_y[i])

        if grid_index not in grid_points:
            grid_points[grid_index] = []

        grid_points[grid_index].append(i)  # Store the index of the point

    #Calculate the number of points in each grid cell
    grid_point_counts = {grid_index: len(points) for grid_index, points in grid_points.items()}

    #Identify the grid cell with the maximum and minimum number of points
    max_points_grid = max(grid_point_counts, key=grid_point_counts.get)
    min_points_grid = min(grid_point_counts, key=grid_point_counts.get)

    #Calculate the target number of points for each grid cell
    target_point_count = (grid_point_counts[max_points_grid] - grid_point_counts[min_points_grid]) // 4

    #Create a mask to filter out points exceeding the target count in each grid cell
    mask = np.zeros(len(inFile.points), dtype=bool)

    for grid_index, points in grid_points.items():
        if len(points) > target_point_count:
            mask[points[:target_point_count]] = True

    #Filter the points based on the mask
    filtered_points = inFile.points[mask]                

    return {
        "message": "Hello, World!",
        "data": filtered_points,
    }







# import laspy
# import numpy as np
# import matplotlib.pyplot as plt
# # from mpl_toolkits.mplot3d import Axes3D

# # import matplotlib.pyplot as plt
# from PIL import Image
# import io

# @app.get("/las")
# async def read_las():

#     # Sample data
#     x = [1, 2, 3, 4, 5]
#     y = [2, 3, 5, 7, 11]
#     z = [1, 4, 9, 16, 25]
#     rgb = ['red', 'green', 'blue', 'yellow', 'orange']

#     # Plotting the data
#     fig, ax = plt.subplots()
#     ax.scatter(x, y, s=z, c=rgb, alpha=0.5)

#     # Save the plot as an image
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)

#     # Create a PIL Image from the plot
#     img = Image.open(buffer)

#     # Provide a download link to the user
#     img.save('plot.png')  # Save the image locally
#     print("Plot saved as 'plot.png'. Provide this link to download the image: 'plot.png'")

#     return {
#         "message": "Hello, World!",
#         "data": img,
#     }
    # def plot_las_point_cloud(file_path, output_file):
    #     # Read LAS file
    #     las_file = laspy.read(file_path)

    #     # Extract x, y, z coordinates
    #     x = las_file.x
    #     y = las_file.y
    #     z = las_file.z

    #     # Extract RGB values (if available)
    #     if hasattr(las_file, 'red') and hasattr(las_file, 'green') and hasattr(las_file, 'blue'):
    #         red = las_file.red
    #         green = las_file.green
    #         blue = las_file.blue
    #         colors = np.column_stack((red, green, blue)) / 65535.0  # Normalize to [0, 1]
    #     else:
    #         colors = None

    #     # Plot point cloud
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')

    #     # If RGB colors are available, use them for coloring the points
    #     if colors is not None:
    #         sc = ax.scatter(x, y, z, c=colors, marker='.')
    #         ax.set_xlabel('X Label')
    #         ax.set_ylabel('Y Label')
    #         ax.set_zlabel('Z Label')
    #     else:
    #         ax.scatter(x, y, z, c='b', marker='.')

    #     # Save plot to output file
    #     return plt.savefig()
    # # Example usage
    # file = plot_las_point_cloud('../app/data/uploads/Left_Rocks21.las', 'point_cloud_plot.png')

    # return {
    #     "message": "Hello, World!",
    #     "data": file,
    # }


