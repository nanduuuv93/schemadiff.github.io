-- base query

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

-- added Primary Key Index

select concat('CREATE TABLE', ' ', col.TABLE_NAME, '(',
              group_concat(
                      col.COLUMN_NAME, ' ',
                      if(col.Extra = 'auto_increment', concat(col.COLUMN_TYPE, ' ', 'auto_increment'), col.column_type),
                      ' ',
                      if(col.CHARACTER_SET_NAME is not null,
                         concat('character set', ' ', CHARACTER_SET_NAME, ' ', 'collate', ' ', COLLATION_NAME), ''),
                      ' ',
                      if(col.IS_NULLABLE = 'NO', 'NOT NULL', ''),
                      if(col.COLUMN_DEFAULT is not null, concat('default', ' ', "'", col.COLUMN_DEFAULT, "'"), '')
                  ), ' ', ',',
              concat(
                      case
                          when col.COLUMN_KEY = 'PRI' then concat('PRIMARY KEY', ' ', '(', col.COLUMN_NAME, ')')
                          when con.CONSTRAINT_TYPE = 'UNIQUE' then concat('constraint', ' ', CONSTRAINT_NAME, ' ',
                                                                          'unique key', ' ',
                                                                          '(', col.COLUMN_NAME, ')')
                          end
                  ),
              ')')
from information_schema.COLUMNS col
         inner join information_schema.TABLE_CONSTRAINTS con
                   on col.TABLE_SCHEMA = con.TABLE_SCHEMA
                       and col.TABLE_NAME = con.TABLE_NAME
                      -- and col.COLUMN_KEY = substr(con.CONSTRAINT_TYPE, 1, 3)
where col.TABLE_SCHEMA = 'iot_wb' and col.TABLE_NAME in ('logs');

-- added unique indexes
