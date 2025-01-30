from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from copy import deepcopy
from datetime import datetime
import os 
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, FloatType, LongType, DoubleType, BooleanType
from outscraper import ApiClient

def _get_logger(_path=None):
    raise ValueError('Must define logger')

def get_cols(catalog:str, database:str, table:str):
    """Get columns from delta table
    
    Args:
        catalog (str): Catalog name
        database (str): Database name
        table (str): Table name
        
    Returns:
        cols [str]: List of column names
        
    """
    spark = SparkSession.builder.getOrCreate()
    spark.catalog.setCurrentCatalog(catalog)
    cols = spark.sql(f'SHOW COLUMNS IN {table} in {database};').select('col_name').rdd.flatMap(lambda x: x).collect()
    return cols

    
def compare_cols(source_cols:list, dest_cols:list):
    """Compare source and destination columns
    
    Args:
        source_cols (list): List of source columns
        dest_cols (list): List of destination columns
        
    Returns:
        just_source, just_dest, both (list):
            just_source: Columns only in source
            just_dest: Columns only in destination
            both: Columns in both source and destination"""
    #Ignore, these are auto set
    dest_cols=[col for col in dest_cols if col not in ['CreatedDate', 'CreatedBy']]

    just_source = [col for col in source_cols if col not in dest_cols]
    just_dest = [col for col in dest_cols if col not in source_cols]
    both = [col for col in source_cols if col in dest_cols]
    return just_source, just_dest, both

def insert_data(df, catalog, database, table, col_truth='DESTINATION', logger=None):
    """Insert data into delta table

    Args:   
        df (pyspark.sql.dataframe.DataFrame): Dataframe to insert into delta table
        catalog (str): Catalog name
        database (str): Database name
        table (str): Table name
        col_truth (str, optional): Which columns to use as truth. Defaults to 'DESTINATION'.
            Valid values are 'DESTINATION' and 'SOURCE'
    
    Returns:
        count (int): Number of rows inserted into delta table
    
    """
    #if logger is None:
    #    logger = _get_logger()
    reserved_cols = ['OPERATION', 'SINK_ID']
    if 'id' in df.columns:
        raise ValueError('id column found in dataframe. id is a reserved column name. Please rename id column to something descriptive to the specific table.')

    destination_cols = get_cols(catalog, database, table)
    just_source, just_dest, both = compare_cols(df.columns, destination_cols)
    if col_truth == 'DESTINATION':
        #NOTE we use both and not just_dest because we want the destination to use defaults where applicable
        df= df.select(both)
    elif col_truth == 'SOURCE':
        raise NotImplementedError('SOURCE not implemented yet, will not until really good reason.')
        #TODO add ability to merge schema by creating new columns in destination based on source
    else:
        raise ValueError(f'col_truth {col_truth} not recognized. Valid values are DESTINATION and SOURCE')
    #if just_source:
    #    logger.log('WARNING', f'The following columns were not found in the destination table: {", ".join(just_source)}')
    #logger.log('INFO', f'The following cols are in the destination, but not in the source: {", ".join(just_dest)}')

    #remove reserved columns that are used by other operations
    for col in reserved_cols:
        if col in df.columns:
            df = df.drop(col)
    
    spark = SparkSession.builder.getOrCreate()
    spark.catalog.setCurrentCatalog(catalog)
    df.write.mode("append").saveAsTable(f'{database}.{table}')
    #logger.log('INFO', f'Inserted {df.count()} rows into {catalog}.{database}.{table}')
    return df.count()

from _thread import get_ident

def recursive_repr(fillvalue='...'):
    'Decorator to make a repr function return fillvalue for a recursive call'

    def decorating_function(user_function):
        repr_running = set()

        def wrapper(self):
            key = id(self), get_ident()
            if key in repr_running:
                return fillvalue
            repr_running.add(key)
            try:
                result = user_function(self)
            finally:
                repr_running.discard(key)
            return result

        # Can't use functools.wraps() here because of bootstrap issues
        wrapper.__module__ = getattr(user_function, '__module__')
        wrapper.__doc__ = getattr(user_function, '__doc__')
        wrapper.__name__ = getattr(user_function, '__name__')
        wrapper.__qualname__ = getattr(user_function, '__qualname__')
        wrapper.__annotations__ = getattr(user_function, '__annotations__', {})
        return wrapper

    return decorating_function

class partial:
    """New function with partial application of the given arguments
    and keywords.
    """

    __slots__ = "func", "args", "keywords", "__dict__", "__weakref__"

    def __new__(cls, func, /, *args, **keywords):
        if not callable(func):
            raise TypeError("the first argument must be callable")

        if hasattr(func, "func"):
            args = func.args + args
            keywords = {**func.keywords, **keywords}
            func = func.func

        self = super(partial, cls).__new__(cls)

        self.func = func
        self.args = args
        self.keywords = keywords
        return self

    def __call__(self, /, *args, **keywords):
        keywords = {**self.keywords, **keywords}
        return self.func(*self.args, *args, **keywords)

    @recursive_repr()
    def __repr__(self):
        qualname = type(self).__qualname__
        args = [repr(self.func)]
        args.extend(repr(x) for x in self.args)
        args.extend(f"{k}={v!r}" for (k, v) in self.keywords.items())
        if type(self).__module__ == "functools":
            return f"functools.{qualname}({', '.join(args)})"
        return f"{qualname}({', '.join(args)})"

    def __reduce__(self):
        return type(self), (self.func,), (self.func, self.args,
               self.keywords or None, self.__dict__ or None)

    def __setstate__(self, state):
        if not isinstance(state, tuple):
            raise TypeError("argument to __setstate__ must be a tuple")
        if len(state) != 4:
            raise TypeError(f"expected 4 items in state, got {len(state)}")
        func, args, kwds, namespace = state
        if (not callable(func) or not isinstance(args, tuple) or
           (kwds is not None and not isinstance(kwds, dict)) or
           (namespace is not None and not isinstance(namespace, dict))):
            raise TypeError("invalid partial state")

        args = tuple(args) # just in case it's a subclass
        if kwds is None:
            kwds = {}
        elif type(kwds) is not dict: # XXX does it need to be *exactly* dict?
            kwds = dict(kwds)
        if namespace is None:
            namespace = {}

        self.__dict__ = namespace
        self.func = func
        self.args = args
        self.keywords = kwds

try:
    from _functools import partial
except ImportError:
    pass

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')
WRAPPER_UPDATES = ('__dict__',)
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)

def format_write_info(table, operation='INSERT'):
    def decorator(func): 
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper function to rename columns in the data.
            Args:
                *args: Positional arguments passed to the decorated function.
                **kwargs: Keyword arguments passed to the decorated function.
                client: Client name to replace '[CLIENT]' in the table name when used with reusable functions.

            Returns:
                dict: Write infor dictionary consumed by custom logger.
            """
            new_table = table #NOTE must do this becuase table will get overloaded in conditional otherwise. Ask Jeb or Arby why.
            if 'client' in kwargs and '[CLIENT]' in new_table:
                new_table = table.replace('[CLIENT]', kwargs['client'])

            if operation == 'INSERT':
                insert_count = func(*args, **kwargs)
                return {'table': new_table, 
                        'operation': 'insert', 
                        'insert_count': insert_count
                        }
            if operation == 'UPSERT':
                insert_count, update_count, delete_count, ignore_count = func(*args, **kwargs)
                return {'table': new_table, 
                        'operation': 'upsert', 
                        'insert_count': insert_count,
                        'update_count': update_count,
                        'delete_count': delete_count,
                        'ignore_count': ignore_count
                        }
            if operation == 'PSEUDO_UPSERT':
                insert_count, update_count, delete_count, ignore_count = func(*args, **kwargs)
                return {'table': new_table, 
                        'operation': 'pseudo_upsert', 
                        'insert_count': insert_count,
                        'update_count': update_count,
                        'delete_count': delete_count,
                        'ignore_count': ignore_count
                        }
            raise ValueError(f'Invalid operation type {operation}. Valid are INSERT, UPSERT, PSEUDO_UPSERT')
        return wrapper
    return decorator

places_raw_response_schema = {
    'place_id': None,
    'response': None
}

places_places_schema = {
    'place_id': None,
    "query": None,
    "name": None,
    "google_id": None,
    "latitude": None,
    "longitude": None,
    "full_address": None,
    "country": None,
    "city": None,
    "state": None,
    "site": None,
    "phone": None,
    "category": None,
    "type": None,
    "subtypes": None,
    "rating": None,
    "reviews": None,
    "reviews_per_score": None,
    "reviews_link": None,
    "reviews_id": None,
    "working_hours": None,
    "owner_id": None,
    "verified": None,
    "owner_title": None,
    "owner_link": None,
    "location_link": None,
    "location_reviews_link": None,
    "about": None
}

places_reviews_schema = {
    'place_id': None,
    "google_id": None,
    "review_id": None,
    "author_link": None,
    "author_title": None,
    "author_id": None,
    "author_reviews_count": None,
    "author_ratings_count": None,
    "review_text": None,
    "review_questions": None,
    "owner_answer": None,
    "owner_answer_timestamp": None,
    "owner_answer_timestamp_datetime_utc": None,
    "review_link": None,
    "review_rating": None,
    "review_timestamp": None,
    "review_datetime_utc": None,
    "review_likes": None,
    "reviews_id": None
}

places_traffic_schema = {
    "place_id": None,
    "day": None,
    "hour": None,
    "time": None,
    "percentage": None,
    "title": None
}

PlacesRawResponseSchema = StructType([
    StructField("place_id", StringType(), True),
    StructField("response", StringType(), True)
])

PlacesPlacesSchema = StructType([
    StructField("place_id", StringType(), False),
    StructField("query", StringType(), True),
    StructField("name", StringType(), True),
    StructField("google_id", StringType(), True),
    StructField("latitude", DoubleType(), True),
    StructField("longitude", DoubleType(), True),
    StructField("full_address", StringType(), True),
    StructField("country", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("site", StringType(), True),
    StructField("phone", StringType(), True),
    StructField("category", StringType(), True),
    StructField("type", StringType(), True),
    StructField("subtypes", StringType(), True),
    StructField("rating", FloatType(), True),
    StructField("reviews", IntegerType(), True),
    StructField("reviews_per_score", StringType(), True),
    StructField("reviews_link", StringType(), True),
    StructField("reviews_id", StringType(), True),
    StructField("working_hours", StringType(), True),
    StructField("owner_id", StringType(), True),
    StructField("verified", BooleanType(), True),
    StructField("owner_title", StringType(), True),
    StructField("owner_link", StringType(), True),
    StructField("location_link", StringType(), True),
    StructField("location_reviews_link", StringType(), True),
    StructField("about", StringType(), True)
])

PlacesReviewsSchema = StructType ([
    StructField("place_id", StringType(), True),
    StructField("google_id", StringType(), True),
    StructField("review_id", StringType(), True),
    StructField("author_link", StringType(), True),
    StructField("author_title", StringType(), True),
    StructField("author_id", StringType(), True),
    StructField("author_reviews_count", IntegerType(), True),
    StructField("author_ratings_count", IntegerType(), True),
    StructField("review_text", StringType(), True),
    StructField("review_questions", StringType(), True),
    StructField("owner_answer", StringType(), True),
    StructField("owner_answer_timestamp", LongType(), True),
    StructField("owner_answer_timestamp_datetime_utc", StringType(), True),
    StructField("review_link", StringType(), True),
    StructField("review_rating", IntegerType(), True),
    StructField("review_timestamp", LongType(), True),
    StructField("review_datetime_utc", StringType(), True),
    StructField("review_likes", IntegerType(), True),
    StructField("reviews_id", StringType(), True)
])

PlacesTrafficSchema = StructType ([
    StructField("place_id", StringType(), True),
    StructField("day", StringType(), True),
    StructField("hour", IntegerType(), True),
    StructField("time", StringType(), True),
    StructField("percentage", IntegerType(), True),
    StructField("title", StringType(), True)
])

class OutscraperInterface:
    def __init__(self, key, place_name):
        """A class to interface with the Outscraper API.

        Args:
            place_name (str): A google maps search query akin to searching results on google maps or a google place ID or a list of queries.

        Reference:
            API Reference: https://outscraper.com/google-maps-reviews-api/
            Parameters: https://app.outscraper.com/api-docs#tag/Google/paths/~1maps~1reviews-v3/get
            Starter Code: https://github.com/outscraper/outscraper-python/blob/master/examples/Google%20Maps%20Reviews.md
        """
        self.raw = None
        self.places = None
        self.reviews = None
        self.traffic = None
        self._max_iter = 10000
        self._place_name = place_name 
        self.client = ApiClient(api_key= key)

    @property
    def place_name(self):
        return self._place_name
    
    @place_name.setter
    def place_name(self, place_name):
        if self._place_name != place_name:
            self.raw = None
            self.places = None
            self.reviews = None
            self.traffic = None
            self._place_name = place_name

    def get_reviews_by_query(self, review_amount, result_amount=1, cutoff=None):
        """Get the reviews of one or more attractions based on a google maps search query.
        
        Args:
            result_amount (int): The amount of attractions a user would like to see from the query.
            review_amount (int): The amount of reviews a user would like to see for each result, sorted by newest reviews first.
            cutoff (datetime) (optional): A timestamp for the cutoff date to recieve reviews. All reviews will be after this timestamp.
            
        Returns:
            results: A list containing detailed user reviews of the given search results.
        """
        if cutoff is not None and not isinstance(cutoff, int):
            cutoff = int(cutoff.timestamp())
        results = self.client.google_maps_reviews(self._place_name, reviews_limit=review_amount, limit=result_amount, sort='newest', cutoff=cutoff, language='en')
        return results
    
    def _map_results_to_schema(self, result, schema, place_id, day=None): 
        """Maps results from Outscraper API to a schema

        Args:
            result (dict): Result from Outscraper API
            schema (dict): Schema to map results to
            place_id (str): Place ID to add to result (taken out individually to allow place_id to be used in every schema)

        Returns:
            row (dict): Row mapped to schema
        """
        row = deepcopy(schema)
        for k in row:
            if k == 'place_id':
                row[k] = place_id
            elif k == 'day':
                row[k] = day
            elif k == 'response':
                row[k] = str(result)
            # Google reviews change 'rating' results to int if it is a whole number (ex: 4.0 -> 4).
            # This conditional prevents type discrepencies in Spark
            elif k == 'rating':
                row[k] = float(result[k]) if result[k] is not None else None
            else:
                row[k] = result[k] if (not isinstance(result[k], dict) and not isinstance(result[k], list)) else str(result[k])
        return row
    
    def get_raw_info(self, review_amount, result_amount=1, cutoff=None):
        """Runs an outscraper query and transfoms the raw data into a fact table format.

        Args:
            review_amount (int): Amount of reviews returned. Defaulted to one because reviews will not show in this table.
            result_amount (int): Amount of query results to return.
            cutoff (datetime) (optional): A timestamp for the cutoff date to recieve reviews. All reviews will be after this timestamp.

        Returns:
            raw [dict]: List of raw response from API
        """
        if cutoff is not None and not isinstance(cutoff, int):
            cutoff = int(cutoff.timestamp())
        if self.raw is None:
            self.get_full_places(review_amount, result_amount, cutoff) 
        return self.raw
    
    def get_place_info(self, result_amount, review_amount=1):
        """Runs an outscraper query and transfoms the raw place data into a fact table format.

        Args:
            result_amount (int): Amount of query results to return.
            review_amount (int): Amount of reviews returned. Defaulted to one because reviews will not show in this table.
            
        Returns:
            places [dict]: List of place data flattened from raw
        """
        if self.places is None:
            self.get_full_places(review_amount, result_amount)
        return self.places

    def get_reviews_info(self, review_amount, result_amount = 1, cutoff=None):
        """Runs an outscraper query and transfoms the raw review data into a fact table format.

        Args:
            review_amount (int): Amount of reviews returned. Defaulted to one because reviews will not show in this table.
            result_amount (int): Amount of query results to return.
            cutoff (datetime) (optional): A timestamp for the cutoff date to recieve reviews. All reviews will be after this timestamp.
 
        Returns:
            reviews [dict]: List of review data flattened from place
        """
        if cutoff is not None and not isinstance(cutoff, int):
            cutoff = int(cutoff.timestamp())
        if self.reviews is None:
            self.get_full_places(review_amount, result_amount, cutoff)
        return self.reviews
    
    def get_traffic_info(self, result_amount, review_amount = 1):
        """Runs an outscraper query and transfoms the raw traffic data into a fact table format.

        Args:
            review_amount (int): Amount of reviews returned. Defaulted to one because reviews will not show in this table.
            result_amount (int): Amount of query results to return.
 
        Returns:
            traffic [dict]: List of traffic data flattened from place
        """

        if self.traffic is None:
            self.get_full_places(review_amount, result_amount)
        return self.traffic
    
    def get_full_places(self, review_amount, result_amount, cutoff=None):
        """Runs an outscraper query and modifies self.raw, self.places, self.reviews with data in a fact table format.

        Args:
            review_amount (int): Amount of reviews returned. 0 returns all reviews.
            result_amount (int): Amount of query results to return.
            cutoff (datetime) (optional): A timestamp for the cutoff date to recieve reviews. All reviews will be after this timestamp.

        Returns:
            raw [dict]: List of raw response from API
            places [dict]: List of place data flattened from raw
            reviews [dict]: List of review data flattened from place
            traffic [dict]: List of traffic data flattened from place
        """
        raw = []
        places = []
        reviews = []
        traffic = []
        if cutoff is not None and not isinstance(cutoff, int):
            cutoff = int(cutoff.timestamp())
        if self.raw is None or self.places is None or self.reviews is None:
            results = self.get_reviews_by_query(review_amount, result_amount, cutoff)
            for result in results:
                raw.append(self._map_results_to_schema(result, places_raw_response_schema, result['place_id']))
                places.append(self._map_results_to_schema(result, places_places_schema, result['place_id']))
                for review in result['reviews_data']:
                    reviews.append(self._map_results_to_schema(review, places_reviews_schema, result['place_id']))
                if result['popular_times']:
                    for day in result['popular_times']:
                        if day['day'] != 'live':
                            for time in day['popular_times']:
                                traffic.append(self._map_results_to_schema(time, places_traffic_schema, result['place_id'], day['day']))
        if self.raw is None:
            self.raw = raw
        if self.places is None:
            self.places = places
        if self.reviews is None:
            self.reviews = reviews
        if self.traffic is None:
            self.traffic = traffic
        return self.raw, self.places, self.reviews, self.traffic

    