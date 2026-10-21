/*
StormPK EU: adapt the historical 2022 GameDB QuestList schema to the current
PristonTale-EU-main server's quest query.

Run using a sysadmin connection with GameDB backed up. Never execute this
against unrelated databases. Idempotent: only adds missing columns.
There is no destructive DDL and existing quest rows/columns are preserved.

Legacy quest data is used to populate the four missing quest-book text
columns. Other new fields default to 0 or empty strings until the complete
EU content is supplied; this makes existing quests load but cannot recreate
absent upstream quest definitions.
*/
USE [GameDB];

IF OBJECT_ID(N'dbo.QuestList',N'U') IS NULL
    THROW 51000, 'StormPK migration aborted: dbo.QuestList is missing', 1;

SET XACT_ABORT ON;
BEGIN TRY
    BEGIN TRANSACTION;

    IF COL_LENGTH(N'dbo.QuestList',N'MainQuestID') IS NULL
        ALTER TABLE dbo.QuestList
            ADD MainQuestID int NOT NULL
                CONSTRAINT DF_StormPK_QuestList_MainQuestID DEFAULT (0) WITH VALUES;

    IF COL_LENGTH(N'dbo.QuestList',N'ASMQuestBit') IS NULL
        ALTER TABLE dbo.QuestList
            ADD ASMQuestBit int NOT NULL
                CONSTRAINT DF_StormPK_QuestList_ASMQuestBit DEFAULT (0) WITH VALUES;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookName') IS NULL
    BEGIN
        ALTER TABLE dbo.QuestList ADD QuestBookName varchar(64) NULL;
        UPDATE dbo.QuestList SET QuestBookName = LEFT(COALESCE(Name,''),64);
    END;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookStartText') IS NULL
    BEGIN
        ALTER TABLE dbo.QuestList ADD QuestBookStartText varchar(2048) NULL;
        UPDATE dbo.QuestList SET QuestBookStartText = LEFT(COALESCE(Description,''),2048);
    END;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookTipText') IS NULL
    BEGIN
        ALTER TABLE dbo.QuestList ADD QuestBookTipText varchar(2048) NULL;
        UPDATE dbo.QuestList SET QuestBookTipText = LEFT(COALESCE(ProgressText,''),2048);
    END;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookEndText') IS NULL
    BEGIN
        ALTER TABLE dbo.QuestList ADD QuestBookEndText varchar(2048) NULL;
        UPDATE dbo.QuestList SET QuestBookEndText = LEFT(COALESCE(ConclusionText,''),2048);
    END;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookGroupID') IS NULL
        ALTER TABLE dbo.QuestList
            ADD QuestBookGroupID varchar(32) NOT NULL
                CONSTRAINT DF_StormPK_QuestList_QuestBookGroupID DEFAULT ('') WITH VALUES;

    IF COL_LENGTH(N'dbo.QuestList',N'QuestBookGroupRank') IS NULL
        ALTER TABLE dbo.QuestList
            ADD QuestBookGroupRank int NOT NULL
                CONSTRAINT DF_StormPK_QuestList_QuestBookGroupRank DEFAULT (0) WITH VALUES;

    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
    THROW;
END CATCH;

SELECT COUNT(*) AS QuestRows,
       COUNT(QuestBookName) AS QuestBookTitles,
       COUNT(QuestBookStartText) AS QuestBookStartTexts
FROM dbo.QuestList;
