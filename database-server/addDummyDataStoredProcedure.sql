-- Tell which database to use
USE cs419;

-- Drop stored procedure if it exists
DROP PROCEDURE IF EXISTS spAddDummyData;

DELIMITER $$
-- Start stored procedure
CREATE PROCEDURE spAddDummyData ()
BEGIN

-- insert administrators
INSERT INTO admins (email, password, salt) VALUES ('dhusek@oregonstate.edu', 'a695df4a5805140f21f024e0b30d97657c37f3cbd92f01b8b7b68e9d3d12b6801d3e1aa59deedfafa8d845ebf3f3d444b597d6356ef4cbf387cd71c483e4ee578ccf977c9040d6ec9a4f7dbf90afab47289600142a1b2d146996ebd11f6a1096e8cb594a1e00d8e1f981c7c1cc3d52642ba1c5873fbd3fc6f540d60eb85ed762eefc5098a36a245dd2c1eeb58cfcb797d3f75a933ef94b170a8935f8611e1e7b7f0c991dd8a980cdb2ccccfcf01bb57ec8e6c356fa7209a447a9726b11f4ccb522147daa15928bff23cef244b12747fa61d0db4adcea943343d22322142282ebc1dc94b40090ad7b159ee6111ed56d6bc4a1ddb6bb532da7e538f813030e1291aabe291524a182eee0274f3e4d50ba936e79d7b9f3439ddf53fc3b82a19df719605d2b04d9ac65c0745abbbb9e41c64e63d26792fd570d4acae9b06de747bfdffbf5ba1f50ba86e06753e77123141462723511fa3093212dbbb02d2ca169905bb0ae8b8987856637c2116b64b01642faf582bd7195980f6952c016ffdd5170541020f0a9f2bf7367e1ad3b8b729ae6418a63d1189282c030f3fd804f0a469bfe5748bdecee1b902e74a8182b59594d5ba7d3feb8a9f6f5e95d69f1bb8d6fab4f8e13f544c4aabd47005f422305cc4cadde5a128c9e386a5e7edc39ce62a18cfeee47d648ed353bba44f6c5b9db7f0fe6ba0b50945bf97185e9a9622fb55aece1', '92cccf968bb85868741eb87742a661cb');
INSERT INTO admins (email, password, salt) VALUES ('hallbry@oregonstate.edu', '0d758941c4ccb182ca0546aaaa6da244610787b7f86d4017fd767887e1d39da39cb7fa1bde6c34b51227cd9e8bf154534f35635ea5cf77aefefbe18f9b13f2295a41dab70aaacc5fa620ec14b2e51cba37b581374abfef2b8dd0af558ee57a8178e3bc12faf9603f6f5065278cf9cd98b1282e40c35b06391813d0dd4c91ff137611b6052bdc0487299b12abcee88f4d70d1a42638e922b7cad9202e2178f36e2dae34bd6198c396603491b3ecad0c69a9742e8c64d78c1ae20f6a7a75ff64d0d30edc251dc7321c3f3fe9c763e7359a795d9e0ddc56028186e89d700ccc9801310b71445774315df196b332f7af93dd28416a2224165c5e94543a92d3fc58f34bbba627c2fab64844296ed27d35ae0c076c8b3ab2e73e77e6ce1a5096e23fb4aee24c7ac44993ad082916e35a459ed78bcadcb825a1bece10825821ad296a2314eaa5d25ab04e752a95bdd0b32aac8e006f4b29343a1d862305a94a05b4fa1fc5515e1044366a5fd80378f5b1371d0e655ee9498f56063a5770db42a95ab63e314726bfcae0fd7c0c77fc16f7976c0d85e13daa51d56f6c757e86d868dae7d4186954b017c75c976ef6eed4301561c3dc24c24434f272a94d032ee887c2fdf873c3a10bdb0a60a588f6632b7705959c48d2f1652c7fdbdfed88a18aecc4d7ca959924b34b83973b9776a775d8c9d9162d880371dd5e156478cf0cbb515848f5', '4477bf3ce503ef6e722fa2bf48a499ec');
INSERT INTO admins (email, password, salt) VALUES ('mccumstw@oregonstate.edu', '7a5099352d8d6022b06d4d25820d3fc5ded37a02b4ad12d45c7ee84a9a7138c72bf6896a29c6d75e25d7e532df09d8cb8087f133e2fd5442e2c8fdf38de4dedf9b073aa96cf5f033011d6a46b0fd8b18928911b7ab81e6a091c430461ecf9897f83df82235409434d28f7e02f43806cb734ba449682fc967f8ede753a1179811ed6c161e544e0bc03724748e5565ac08797841da53291aaa4f29dcbe4f7a42565f3c6722ca33f52dd7c0f86dff66d24c3356ba4884deab43ac6b7379764f8f630defd6ca95dd8a398401c2d856cb80f65baed0f65f85243b8f6820188f272d529d64a9b79754963da097ffb8836487eaac64a364a87d23dd587a3fc2a67b0628c065c844b32e84fbabd88ff553c3a6ad448c17564ba865b574ab91ef56599b2b1f1aec2583e3fa8b0d3557a8abc6db3607a43fac6fa2c060b6b9c844123530616768f957ce91c440e8a750459086ef6ffda541a55585fa59a7f688c7c54b198205bf9e779a19620a3d0152e9e1a019e05e82de2c2484b35d88cfbac0314e5d7fa6a1e1f71b3788a1b0801dd26939b6b750464b2e21fe7063da2274803d97b45e6eeb4e51ec6e18e1a273dca5f2c32a705131daa8912dd0e3cffe799887e363cd6733a6ea73708888c099c25402cb1283f759e093940336826cee619daf5b47d1e50da02fbf8e9ff9806fc4d187b1385c6c23814330ea24993a891379e07b7442', '92fd7c4480ece15f56e38ada787b8a11');


-- insert award types
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Week', 1);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Month', 10);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Employee of the Year', 100);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Gold Star Employee', 20);
INSERT INTO awardTypes (name, prestigeLevel) VALUES ('Silver Star Employee', 10);


-- insert users
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('Kristen', 'dhusek@oregonstate.edu', 'dc88c97104e2881aa5c12fc99fc5c2ad1bf57542b2d8adfc0a03c6c1f8654001121f1eae0116bdd48d86863b77d5b24a1ee03e383ca1b442191e168cb56a3e17efff9463689d063ed8a049b969fdfe77cabf70cc438efe445df65da4c056954a532cc04e539d22626900a652f8656f955d868325de613acd7a216187a8e0228d37043a26d46465352045ce804882c790157289eef66b367a0762d0f60884ffdcc5f99c35cd5271b02e0e4814e449f3296ed439364ca292ec4f5f986471002009efca006d2c32929aaf7e0e0d1d51f52c1c1b87f74aa9224141433dc03882d5f1419c57889dfef580c0fda2d03608a733c6f8694b04b76eb3ecbadb1f76c69f80f475ada94d7ce67732c2c465e3a0965796fa1b81bf4cace7bdde5a75d64e7c5b50f9440e9119c806fbed51d13c9401162e18e709cdcc0a6d66b84ad7a9e2007cb55e7a622286fa54cb05a4e07afa7e53d31a00ec9e7ffdbea527941f1de3ac69e7364382456730c449b10a6b54ffd8a8837f6109dda9ca087aacff08fec396640d7cda507d6c5726314069eee56cbb5cb705394d8f251e347bc0cf610b5f4b9a0bb61fe737d87ffadc6041acc0884910dfcc5dfd35e4bb41ef2f27336d84d6c2b366c3c91b82bee6d69636ef45ebaf5eaa08f406ab3c71a2bf392968658a92c41eb807c12270c685b1943c7af7cd6c651b279a1eaa362aaf858c60de029ca683', '3b931052f45862f4b6e192b97f3ed1fa', 'kristen d', 'Washington', '2015-07-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('Bryant', 'hallbry@oregonstate.edu', 'a3cb623c1a65c6b6e0108d5b6727a700df5730c5e3dc1fb9fe1cbcdac02903ecff576b76ca97d48291d3c56253cfbc8230948de822881324c1b246754a5e8958c2b9f36d13db02f7aa98d0955c22d3576c5679c1f12b77938a517fdd27f454cdaeabe4df13a5afe5363cdc9c46f1fa91a4cf177b71d643d8b6d422c468e6920d22742797cc1aee4d7e49b6137ea1740d43febfaf4588cddff752dad36ef953624bbe937660043a6a3ffdb0cb7493d934dc5014b628f72d1f893dd0dfa80baaa15ceebb31e6637f792647c7370d201ffa40a033ef18537a011d06f2f164c4eb06767f036e6a6779cfa45a195a114f2450513bd7de0130cc21e8dfd947b3dd58864187ae0b56273e2b4cf9618eced6aced42750d84a7d89f7c4e31b4b2aa0c23271ddbef2d64f9aebe049a0782fc0564d6e8b32584e9a4d6dbcbc9c56b86a4161fcb51dfdd0355ea012e1699ef264524dc72ff091ba8ea035854cd35927e4c5f7746567fd887fab7109495f697afb6fef61828508c9b39dde3ac4085ce5ad52aee03b80d14f5d437a143ed2eb5315317e7c805f8e83ecc7a20e9b601a9514f5d23a3eed08a233aceea0ae6b2000232f92e6d9dfd54c8a8d1e554cfaa81b56ebbb304ca39f9e8bd14421e2c4e6a9523737bcb0ed44f2034d4dc351eb5f2acb805122b605da337496a2c7ddb49fb2f6d3866d6e188f2043d13ef1cbd9cdf788d5258', '3feabe89c659bdbf327feac28f923643', 'bryant h', 'Washington', '2014-03-02');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('William', 'mccumstw@oregonstate.edu', '89f84a853420f86e6dd32d73437e0f6a87c832dcb4d7302bdef07691c23065916472e99577434497c5e05e494a9f8b9272d444c1c6279481864b48ac8c7bebb2347283cce5e633a641018e8ffb65622fb03df778b69ed66df8911e5dd30bdf97d48377169dc4bce95f9f134e58463875440a442ee195e42a9c0e6ed0968196244fe1900df855877f1cd3e619303fd580c28a2321084bafeb0ddbbfcd5d04fe771fd5ab705ff81c46883a1d02895e55e70e3917a15b7b9d5a0f8e6d5bf922db7b08104887e748c12a15915239c5ee60bb3d068785104c322729650f949eacbb47cfbc11c0a405cb158e1f291690a7c0420c3f57c060bbec83135863aa735916b81c64d47255de86509e2ca45ab189884e78737b201c6d4f7ec698515482da06ae0385d0adc410fd3a42a1559761905ccb5b7d7d9e05f17ed14b9b3dad348ee13f1937b5eed473314e090775a82220ad1226d20a7c0798a72859792f75e02173955be22cc5cfb9ef81145766bf8117132f0b4e74bdc22f57d1b086e96e6f717c0103bc3d40d1714645a91b3d8d6321b8155ac4a2c2c418553905f0bcafdd9498ccc5c4b5b73eec6c5598cb8e56716de1be05374a2acad83bf21e758b8a12792b6c733b3c2f770cae93a949d420143c2a0503104f310bf9af1069b70463067c178e834d327525b57384c7e6eee72ce3ce6a5321295461a5d85dcdf6383631638903', 'ff75efed5e44b227a31ae8b62d1802f1', 'william m', 'Canada', '2015-09-15');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test1', 'test1@test.com', 'a', 'abc', 'nHj0FwC8lsuMBkEY', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test2', 'test2@test.com', 'b', 'abc', 'apmS9KPts8AFxPkJ', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test3', 'test3@test.com', 'c', 'abc', 'Kj729z0nvuYfeJzP', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test4', 'test4@test.com', 'd', 'abc', 'IwGVDD63VIVSbBKl', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test5', 'test5@test.com', 'e', 'abc', '2nFXweFwfZ1uauh9', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test6', 'test6@test.com', 'f', 'abc', 'rmDZBOUoS6ikEusI', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test7', 'test7@test.com', 'g', 'abc', '0D2mzubHMioD9n9P', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test8', 'test8@test.com', 'h', 'abc', 'T3t4TzVs11FUltfQ', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test9', 'test9@test.com', 'i', 'abc', 'CYbDS1m3LklWjlRK', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test10', 'test10@test.com', 'j', 'abc', '525ube3GDULySfrL', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test11', 'test11@test.com', 'k', 'abc', 'Bz1ZeFCEirVvDUY6', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test12', 'test12@test.com', 'l', 'abc', 'qC81arZy9TFT5UxT', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test13', 'test13@test.com', 'm', 'abc', 'nVAJN61whMYosSVG', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test14', 'test14@test.com', 'n', 'abc', 'w5TJ9gikMvy1twEJ', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test15', 'test15@test.com', 'o', 'abc', '3oCGkagXLllGNZFE', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test16', 'test16@test.com', 'p', 'abc', 'E8SgOU8Emw1qfBtT', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test17', 'test17@test.com', 'q', 'abc', '5nu5pG1RY2rPr2av', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test18', 'test18@test.com', 'r', 'abc', 'nZccXEhr9T5xecCr', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test19', 'test19@test.com', 's', 'abc', '3r06A5gHBqDLyTDw', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test20', 'test20@test.com', 't', 'abc', '9fV4M5yqxUMTJr2s', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test21', 'test21@test.com', 'u', 'abc', 'oSJ2JNRgCqyNBGZY', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test22', 'test22@test.com', 'v', 'abc', 'nUjzJlj5bfZxAKDA', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test23', 'test23@test.com', 'w', 'abc', '1w5W6ixysCwQJnHE', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test24', 'test24@test.com', 'x', 'abc', 'iit3fWmjBBxtcrOh', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test25', 'test25@test.com', 'y', 'abc', 'CQBWZ67IKt1PaKAJ', 'US', '2016-09-30');
INSERT INTO users (name, email, password, salt, signatureImage, region, startDate) VALUES ('test26', 'test26@test.com', 'z', 'abc', 'HLpgkYccZ9IBAhqE', 'US', '2016-09-30');


-- insert awards
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 2, 1, '2016-10-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 3, 2, '2016-08-01 13:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 4, '2016-09-01 15:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 1, '2016-10-24 17:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (3, 1, 3, '2016-01-01 14:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 2, 4, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 1, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 2, '2016-03-17 18:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (1, 3, 3, '2016-05-01 13:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 1, 3, '2016-07-01 15:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (2, 3, 2, '2016-02-24 17:30:00');
INSERT INTO awards (receiverID, giverID, typeID, awardDate) VALUES (3, 1, 1, '2016-04-01 14:30:00');

END$$

DELIMITER ;