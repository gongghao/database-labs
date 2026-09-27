package com.example;

import java.sql.*;

public class Main {
    // 注意：路径中使用正斜杠 / 或双反斜杠 \\
    private static final String DB_PATH = "C:\\Users\\passenger\\Documents\\project2.accdb";
    private static final String DB_URL = "jdbc:ucanaccess://" + DB_PATH;

    public static void main(String[] args) {
        try {
            // UCanAccess 驱动（Maven 已引入，无需手动加载，但保留更清晰）
            Class.forName("net.ucanaccess.jdbc.UcanaccessDriver");

            Connection conn = DriverManager.getConnection(DB_URL);
            System.out.println("✅ 成功连接 Access 数据库！");

            // 执行 CRUD
            selectTest(conn);
            conn.close();
            System.out.println("🔌 连接已关闭。");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void selectTest(Connection conn) throws SQLException {
        String sql = "SELECT bname\r\n" + //
                        "FROM Boats\r\n" + //
                        "WHERE bid IN (\r\n" + //
                        "    SELECT bid\r\n" + //
                        "    FROM (\r\n" + //
                        "        SELECT DISTINCT R.sid, R.bid\r\n" + //
                        "        FROM Reserves AS R\r\n" + //
                        "    ) AS DistinctReserves\r\n" + //
                        "    GROUP BY bid\r\n" + //
                        "    HAVING COUNT(*) >= 2\r\n" + //
                        ");\r\n" + //
                        "";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            System.out.println("\n--- 查询结果 ---");
            while (rs.next()) {
                System.out.printf("姓名: %s \n",
                    rs.getString("bname"));
            }
        }
    }
    
}