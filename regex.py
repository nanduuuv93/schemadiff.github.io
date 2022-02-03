import re

schema = """
CREATE TABLE `logs` (
  `_id` int unsigned NOT NULL AUTO_INCREMENT,
  `logsRef` varchar(10) NOT NULL,
  `logHead` varchar(10) DEFAULT NULL COMMENT 'log description',
  `logDesc` text,
  `eventRef` varchar(10) DEFAULT NULL COMMENT 'reference to event mapped to events',
  `severityRef` varchar(10) DEFAULT NULL COMMENT 'reference to severity mapped to severity',
  PRIMARY KEY (`_id`),
  UNIQUE KEY `uq_logsRef` (`logsRef`),
  KEY `ix_logHead` (`logHead`) COMMENT 'key for logHead',
  KEY `fk_eventRef` (`eventRef`),
  KEY `fk_severityRef` (`severityRef`),
  CONSTRAINT `fk_eventRef` FOREIGN KEY (`eventRef`) REFERENCES `events` (`eventRef`),
  CONSTRAINT `fk_severityRef` FOREIGN KEY (`severityRef`) REFERENCES `severity` (`severityRef`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""
pattern = r"(COMMENT.+?),"
replace = re.finditer(pattern, schema)
print(re.sub(pattern, ''.join(','), schema))
