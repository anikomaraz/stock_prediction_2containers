# FROM rocker/r-base:latest
FROM rstudio/plumber

# fetch necessary files
COPY install_packages.R install_packages.R    
COPY plumber.R plumber.R 
COPY plumber_wrapper.R plumber_wrapper.R

# run the script at build
RUN Rscript install_packages.R

# run script when running image
CMD Rscript plumber_wrapper.R

# CMD uvicorn fastapi_:app --host 0.0.0.0 --port $PORT