-- create table

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
                  ), '',
              ')')
from information_schema.COLUMNS col
where col.TABLE_SCHEMA = 'iot_wb'
group by col.TABLE_SCHEMA, col.TABLE_NAME;

-- create table

-- key
select _key.TABLE_NAME,
       concat(group_concat(
               if(_con.CONSTRAINT_TYPE = 'PRIMARY KEY', concat('PRIMARY KEY', ' ', '(', _key.COLUMN_NAME, ')'), ''),
               if(_con.CONSTRAINT_TYPE = 'UNIQUE',
                  concat('CONSTRAINT', ' ', _key.CONSTRAINT_NAME, ' ', 'UNIQUE KEY', ' ', '(', _key.COLUMN_NAME, ')'),
                  ''),
               if(_con.CONSTRAINT_TYPE = 'FOREIGN KEY',
                  concat('CONSTRAINT', ' ', _key.CONSTRAINT_NAME, ' ', 'FOREIGN KEY', ' ', '(', _key.COLUMN_NAME, ')',
                         ' ', 'REFERENCES', ' ', _key.REFERENCED_TABLE_NAME, '(', _key.REFERENCED_COLUMN_NAME, ')')
                   , '')
           ))
from information_schema.KEY_COLUMN_USAGE _key
         inner join information_schema.TABLE_CONSTRAINTS _con
                    on _key.CONSTRAINT_NAME = _con.CONSTRAINT_NAME
                        and _key.CONSTRAINT_SCHEMA = _con.CONSTRAINT_SCHEMA
                        and _key.TABLE_NAME = _con.TABLE_NAME
where _con.TABLE_SCHEMA = 'iot_wb'
  and _con.CONSTRAINT_TYPE in ('UNIQUE', 'PRIMARY KEY', 'FOREIGN KEY')
group by _key.TABLE_NAME;
-- key

