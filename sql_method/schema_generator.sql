select concat('CREATE TABLE', ' ', c.TABLE_NAME, '(',
              group_concat(
                      c.COLUMN_NAME, ' ',
                      if(c.Extra = 'auto_increment', concat(c.COLUMN_TYPE, ' ', 'auto_increment'), c.column_type), ' ',
                      if(c.CHARACTER_SET_NAME is not null,
                         concat('character set', ' ', CHARACTER_SET_NAME, ' ', 'collate', ' ', COLLATION_NAME), ''),
                      ' ',
                      if(c.IS_NULLABLE = 'NO', 'NOT NULL', ''),
                      if(c.COLUMN_DEFAULT is not null, concat('default', ' ', "'", c.COLUMN_DEFAULT, "'"), ''), ' ',
                      if(c.COLUMN_KEY = 'PRI', 'PRIMARY KEY', '')
                  ),
              ')')
from information_schema.COLUMNS c where c.TABLE_SCHEMA in ('iot_wb') group by c.TABLE_SCHEMA, c.TABLE_NAME;
