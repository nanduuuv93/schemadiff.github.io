CREATE TABLE `logs` (
  `_id` int unsigned NOT NULL AUTO_INCREMENT,
  `logsRef` varchar(10) NOT NULL,
  `logHead` varchar(10) DEFAULT NULL,
  `logDesc` text,
  `eventRef` varchar(10) DEFAULT NULL,
  `severityRef` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `uq_logsRef` (`logsRef`),
  KEY `ix_logHead` (`logHead`),
  KEY `fk_eventRef` (`eventRef`),
  KEY `fk_severityRef` (`severityRef`),
  CONSTRAINT `fk_eventRef` FOREIGN KEY (`eventRef`) REFERENCES `events` (`eventRef`),
  CONSTRAINT `fk_severityRef` FOREIGN KEY (`severityRef`) REFERENCES `severity` (`severityRef`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `events` (
  `_id` int unsigned NOT NULL AUTO_INCREMENT,
  `eventRef` varchar(10) NOT NULL,
  `eventType` enum('db','app','network','security') DEFAULT NULL,
  `eventName` varchar(100) DEFAULT NULL,
  `eventDesc` text,
  `severityRef` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `uq_eventRef` (`eventRef`),
  KEY `ix_eventRef` (`eventRef`),
  KEY `ix_severityRef` (`severityRef`),
  CONSTRAINT `fk_severity_ref` FOREIGN KEY (`severityRef`) REFERENCES `severity` (`severityRef`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `severity` (
  `_id` int unsigned NOT NULL AUTO_INCREMENT,
  `severityRef` varchar(10) NOT NULL,
  `severityLevel` enum('ignore','very_low','low','medium','high','very_high') DEFAULT 'ignore' COMMENT 'severity level for activities/logs',
  `severityDesc` text,
  PRIMARY KEY (`_id`),
  UNIQUE KEY `uq_severity_ref` (`severityRef`),
  KEY `ix_severity_ref` (`severityRef`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

select col.TABLE_NAME, /* concat(con.CONSTRAINT_TYPE,' ', con.CONSTRAINT_NAME, ' ','(',col.COLUMN_NAME,')'),*/
       case
           when col.COLUMN_KEY = 'PRI' then concat('PRIMARY KEY', ' ', '(', col.COLUMN_NAME, ')')
           when con.CONSTRAINT_TYPE = 'UNIQUE' then concat('constraint', ' ', CONSTRAINT_NAME, ' ', 'unique key', ' ',
                                                           '(', col.COLUMN_NAME, ')')
           end
    /*col.TABLE_SCHEMA, col.TABLE_NAME, col.COLUMN_NAME, col.COLUMN_KEY, con.CONSTRAINT_NAME, con.CONSTRAINT_TYPE*/
from information_schema.COLUMNS col
         inner join information_schema.TABLE_CONSTRAINTS con
                    on col.TABLE_SCHEMA = con.CONSTRAINT_SCHEMA
                        and col.TABLE_NAME = con.TABLE_NAME
     -- and col.COLUMN_KEY = substr(CONSTRAINT_TYPE, 1, 3)
where col.TABLE_SCHEMA = 'iot_wb'
  and con.CONSTRAINT_TYPE in ('UNIQUE', 'PRIMARY KEY');
