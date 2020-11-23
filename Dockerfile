# Base our image on an official, minimal image of our preferred Ruby
FROM python:3.9.0-slim

# Install essential Linux packages
RUN apt-get update
RUN apt-get install -y curl

RUN pip install --upgrade pip
RUN pip install flask

# Define where our application will live inside the image
ENV APP_ROOT /var/www/grocery-list
ENV FLASK_ENV=development
ENV FLASK_APP=flaskr
ENV SECRET_KEY=development-secret-key

# Set our working directory inside the image
WORKDIR $APP_ROOT

# Use the Gemfiles as Docker cache markers. Always bundle before copying app src.
# (the src likely changed and we don't want to invalidate Docker's cache too early)
# http://ilikestuffblog.com/2014/01/06/how-to-skip-bundle-install-when-deploying-a-rails-app-to-docker/
#COPY Gemfile Gemfile

#COPY Gemfile.lock Gemfile.lock

# Prevent bundler warnings; ensure that the bundler version executed is >= that which created Gemfile.lock
#RUN gem install bundler

# Finish establishing our Ruby enviornment
#RUN bundle install

# Copy the application into place
COPY . .

CMD python -m flask run --host=0.0.0.0
