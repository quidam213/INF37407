-- création de l'utilisateur OGSL
CREATE USER 'ogsl'@'%localhost' IDENTIFIED BY 'ogsl';

-- modifications des droits de l'utilisateur ogsl
GRANT CREATE ROLE ON *.* TO 'ogsl'@'%localhost';
GRANT ROLE_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE USER ON *.* TO 'ogsl'@'%localhost';
GRANT DROP ROLE ON *.* TO 'ogsl'@'%localhost';
GRANT EVENT ON *.* TO 'ogsl'@'%localhost';
GRANT FILE ON *.* TO 'ogsl'@'%localhost';
GRANT PROCESS ON *.* TO 'ogsl'@'%localhost';
GRANT RELOAD ON *.* TO 'ogsl'@'%localhost';
GRANT REPLICATION CLIENT ON *.* TO 'ogsl'@'%localhost';
GRANT REPLICATION SLAVE ON *.* TO 'ogsl'@'%localhost';
GRANT SHOW DATABASES ON *.* TO 'ogsl'@'%localhost';
GRANT SHUTDOWN ON *.* TO 'ogsl'@'%localhost';
GRANT SUPER ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE TABLESPACE ON *.* TO 'ogsl'@'%localhost';
GRANT XA_RECOVER_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT TELEMETRY_LOG_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT TABLE_ENCRYPTION_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT SHOW_ROUTINE ON *.* TO 'ogsl'@'%localhost';
GRANT SET_USER_ID ON *.* TO 'ogsl'@'%localhost';
GRANT SERVICE_CONNECTION_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT SENSITIVE_VARIABLES_OBSERVER ON *.* TO 'ogsl'@'%localhost';
GRANT GROUP_REPLICATION_STREAM ON *.* TO 'ogsl'@'%localhost';
GRANT REPLICATION_SLAVE_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT APPLICATION_PASSWORD_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT SESSION_VARIABLES_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT CLONE_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT CONNECTION_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT SYSTEM_VARIABLES_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT BACKUP_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT AUTHENTICATION_POLICY_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT REPLICATION_APPLIER ON *.* TO 'ogsl'@'%localhost';
GRANT RESOURCE_GROUP_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT SYSTEM_USER ON *.* TO 'ogsl'@'%localhost';
GRANT FIREWALL_EXEMPT ON *.* TO 'ogsl'@'%localhost';
GRANT AUDIT_ABORT_EXEMPT ON *.* TO 'ogsl'@'%localhost';
GRANT BINLOG_ENCRYPTION_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT INNODB_REDO_LOG_ARCHIVE ON *.* TO 'ogsl'@'%localhost';
GRANT ENCRYPTION_KEY_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT PERSIST_RO_VARIABLES_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT BINLOG_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT FLUSH_OPTIMIZER_COSTS ON *.* TO 'ogsl'@'%localhost';
GRANT FLUSH_STATUS ON *.* TO 'ogsl'@'%localhost';
GRANT FLUSH_TABLES ON *.* TO 'ogsl'@'%localhost';
GRANT AUDIT_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT FLUSH_USER_RESOURCES ON *.* TO 'ogsl'@'%localhost';
GRANT GROUP_REPLICATION_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT INNODB_REDO_LOG_ENABLE ON *.* TO 'ogsl'@'%localhost';
GRANT PASSWORDLESS_USER_ADMIN ON *.* TO 'ogsl'@'%localhost';
GRANT RESOURCE_GROUP_USER ON *.* TO 'ogsl'@'%localhost';
GRANT GRANT OPTION ON *.* TO 'ogsl'@'%localhost';

-- suite des modifications des privilèges
GRANT ALTER ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE VIEW ON *.* TO 'ogsl'@'%localhost';
GRANT DELETE ON *.* TO 'ogsl'@'%localhost';
GRANT DROP ON *.* TO 'ogsl'@'%localhost';
GRANT INDEX ON *.* TO 'ogsl'@'%localhost';
GRANT INSERT ON *.* TO 'ogsl'@'%localhost';
GRANT REFERENCES ON *.* TO 'ogsl'@'%localhost';
GRANT SELECT ON *.* TO 'ogsl'@'%localhost';
GRANT SHOW VIEW ON *.* TO 'ogsl'@'%localhost';
GRANT TRIGGER ON *.* TO 'ogsl'@'%localhost';
GRANT UPDATE ON *.* TO 'ogsl'@'%localhost';
GRANT ALTER ROUTINE ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE ROUTINE ON *.* TO 'ogsl'@'%localhost';
GRANT CREATE TEMPORARY TABLES ON *.* TO 'ogsl'@'%localhost';
GRANT EXECUTE ON *.* TO 'ogsl'@'%localhost';
GRANT LOCK TABLES ON *.* TO 'ogsl'@'%localhost';

-- on a donné tous les privilèges mais c'est pas propre je pense, il faudra revoir ça dans le futur
